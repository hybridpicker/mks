# gallery/image_utils.py
"""
Image utility functions for resizing and optimizing uploaded images
to prevent memory limit crashes in the gallery app.
"""

from PIL import Image, ImageOps
import io
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
import logging

logger = logging.getLogger(__name__)

# Configuration
MAX_IMAGE_SIZE = (2048, 2048)  # Maximum width/height in pixels
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes (original upload limit)
JPEG_QUALITY = 85  # JPEG compression quality (1-100)
THUMBNAIL_SIZE = (400, 400)  # Thumbnail dimensions
LAZY_SIZE = (800, 600)  # Lazy loading image dimensions
# Additional configuration for better compression
WEBP_QUALITY = 80  # WebP compression quality for modern browsers
PROGRESSIVE_JPEG = True  # Enable progressive JPEG encoding

def resize_image(image_file, max_size=MAX_IMAGE_SIZE, quality=JPEG_QUALITY):
    """
    Resize an uploaded image file to fit within max_size while maintaining aspect ratio.
    
    Args:
        image_file: Django UploadedFile object
        max_size: Tuple of (max_width, max_height)
        quality: JPEG quality for compression (1-100)
    
    Returns:
        ContentFile object with resized image
    """
    try:
        # Open the image
        img = Image.open(image_file)
        
        # Auto-rotate based on EXIF data (fixes rotation issues from phones)
        img = ImageOps.exif_transpose(img)
        
        # Convert to RGB if necessary (handles PNG with transparency, etc.)
        if img.mode not in ('RGB', 'L'):
            if img.mode == 'RGBA':
                # Create a white background for transparent images
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
                img = background
            else:
                img = img.convert('RGB')
        
        # Get original dimensions
        original_width, original_height = img.size
        max_width, max_height = max_size
        
        # Calculate new dimensions maintaining aspect ratio
        ratio = min(max_width / original_width, max_height / original_height)
        
        # Only resize if the image is larger than max_size
        if ratio < 1:
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            
            # Use high-quality resampling
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            logger.info(f"Resized image from {original_width}x{original_height} to {new_width}x{new_height}")
        
        # Adaptive quality based on file size
        # Start with the configured quality and reduce if needed
        adaptive_quality = quality
        
        # Try different quality settings to get under 2MB
        for attempt_quality in [quality, 80, 70, 60, 50]:
            output_buffer = io.BytesIO()
            
            # Determine format and save
            format_type = 'JPEG'
            if hasattr(image_file, 'name') and image_file.name.lower().endswith('.png'):
                # For very large PNGs, convert to JPEG for better compression
                if original_width * original_height > 2000 * 2000:
                    format_type = 'JPEG'
                    img.save(output_buffer, format=format_type, quality=attempt_quality, optimize=True, progressive=PROGRESSIVE_JPEG)
                else:
                    # Keep PNG format for smaller images
                    format_type = 'PNG'
                    img.save(output_buffer, format=format_type, optimize=True)
            else:
                # Use JPEG for everything else (smaller file size)
                # Enable progressive encoding for better loading experience
                img.save(output_buffer, format=format_type, quality=attempt_quality, optimize=True, progressive=PROGRESSIVE_JPEG)
            
            output_buffer.seek(0)
            file_size = len(output_buffer.getvalue())
            
            # If file is under 2MB, we're done
            if file_size <= 2 * 1024 * 1024:
                adaptive_quality = attempt_quality
                break
            
            # If still too large after lowest quality, resize further
            if attempt_quality == 50 and file_size > 2 * 1024 * 1024:
                # Reduce dimensions by additional 20%
                new_width = int(new_width * 0.8)
                new_height = int(new_height * 0.8)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                logger.info(f"Further resized to {new_width}x{new_height} for size reduction")
        
        # Generate new filename
        original_name = getattr(image_file, 'name', 'image.jpg')
        name_root, name_ext = os.path.splitext(original_name)
        if format_type == 'JPEG' and name_ext.lower() not in ['.jpg', '.jpeg']:
            new_name = f"{name_root}.jpg"
        else:
            new_name = original_name
        
        # Create ContentFile
        resized_file = ContentFile(
            output_buffer.getvalue(),
            name=new_name
        )
        
        logger.info(f"Image processed successfully: {new_name}, size: {len(output_buffer.getvalue())} bytes, quality: {adaptive_quality}")
        return resized_file
        
    except Exception as e:
        logger.error(f"Error resizing image: {str(e)}")
        # Return original file if resizing fails
        return image_file

def create_thumbnail(image_file, size=THUMBNAIL_SIZE):
    """
    Create a thumbnail version of the image.
    
    Args:
        image_file: Django UploadedFile object or ContentFile
        size: Tuple of (width, height) for thumbnail
    
    Returns:
        ContentFile object with thumbnail image
    """
    try:
        # Reset file pointer if it's a file-like object
        if hasattr(image_file, 'seek'):
            image_file.seek(0)
            
        img = Image.open(image_file)
        img = ImageOps.exif_transpose(img)
        
        # Convert to RGB if necessary
        if img.mode not in ('RGB', 'L'):
            if img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            else:
                img = img.convert('RGB')
        
        # Create thumbnail maintaining aspect ratio
        img.thumbnail(size, Image.Resampling.LANCZOS)
        
        # Save to buffer
        output_buffer = io.BytesIO()
        img.save(output_buffer, format='JPEG', quality=80, optimize=True)
        output_buffer.seek(0)
        
        # Generate thumbnail filename
        original_name = getattr(image_file, 'name', 'image.jpg')
        name_root, name_ext = os.path.splitext(original_name)
        thumbnail_name = f"{name_root}_thumb.jpg"
        
        return ContentFile(
            output_buffer.getvalue(),
            name=thumbnail_name
        )
        
    except Exception as e:
        logger.error(f"Error creating thumbnail: {str(e)}")
        return None

def create_lazy_image(image_file, size=LAZY_SIZE):
    """
    Create a lazy loading version of the image (medium size).
    
    Args:
        image_file: Django UploadedFile object or ContentFile
        size: Tuple of (width, height) for lazy image
    
    Returns:
        ContentFile object with lazy loading image
    """
    try:
        # Reset file pointer if it's a file-like object
        if hasattr(image_file, 'seek'):
            image_file.seek(0)
            
        img = Image.open(image_file)
        img = ImageOps.exif_transpose(img)
        
        # Convert to RGB if necessary
        if img.mode not in ('RGB', 'L'):
            if img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            else:
                img = img.convert('RGB')
        
        # Resize maintaining aspect ratio
        original_width, original_height = img.size
        max_width, max_height = size
        
        ratio = min(max_width / original_width, max_height / original_height)
        
        if ratio < 1:
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Save to buffer
        output_buffer = io.BytesIO()
        img.save(output_buffer, format='JPEG', quality=75, optimize=True)
        output_buffer.seek(0)
        
        # Generate lazy filename
        original_name = getattr(image_file, 'name', 'image.jpg')
        name_root, name_ext = os.path.splitext(original_name)
        lazy_name = f"{name_root}_lazy.jpg"
        
        return ContentFile(
            output_buffer.getvalue(),
            name=lazy_name
        )
        
    except Exception as e:
        logger.error(f"Error creating lazy image: {str(e)}")
        return None

def process_uploaded_image(uploaded_file):
    """
    Process an uploaded image by creating all necessary variants.
    
    Args:
        uploaded_file: Django UploadedFile object
    
    Returns:
        Dictionary with processed images:
        {
            'main': ContentFile,      # Resized main image
            'thumbnail': ContentFile, # Thumbnail
            'lazy': ContentFile      # Lazy loading image
        }
    """
    try:
        # First, resize the main image
        main_image = resize_image(uploaded_file)
        
        # Create thumbnail and lazy versions from the main image
        # Reset the main image file pointer
        if hasattr(main_image, 'seek'):
            main_image.seek(0)
        
        thumbnail = create_thumbnail(main_image)
        
        # Reset again for lazy image creation
        if hasattr(main_image, 'seek'):
            main_image.seek(0)
        
        lazy_image = create_lazy_image(main_image)
        
        return {
            'main': main_image,
            'thumbnail': thumbnail,
            'lazy': lazy_image
        }
        
    except Exception as e:
        logger.error(f"Error processing uploaded image: {str(e)}")
        return {
            'main': uploaded_file,
            'thumbnail': None,
            'lazy': None
        }

def check_image_size(image_file, max_size_bytes=MAX_FILE_SIZE):
    """
    Check if an image file is within the size limit.
    
    Args:
        image_file: Django UploadedFile object
        max_size_bytes: Maximum allowed size in bytes
    
    Returns:
        Boolean indicating if file is within size limit
    """
    return image_file.size <= max_size_bytes

def get_image_info(image_file):
    """
    Get information about an image file.
    
    Args:
        image_file: Django UploadedFile object
    
    Returns:
        Dictionary with image information
    """
    try:
        # Reset file pointer if needed
        if hasattr(image_file, 'seek'):
            image_file.seek(0)
            
        img = Image.open(image_file)
        
        # Reset file pointer again for later use
        if hasattr(image_file, 'seek'):
            image_file.seek(0)
            
        return {
            'width': img.width,
            'height': img.height,
            'format': img.format,
            'mode': img.mode,
            'size_bytes': image_file.size if hasattr(image_file, 'size') else 0,
            'size_mb': round(image_file.size / (1024 * 1024), 2) if hasattr(image_file, 'size') else 0
        }
    except Exception as e:
        logger.error(f"Error getting image info: {str(e)}")
        return None
