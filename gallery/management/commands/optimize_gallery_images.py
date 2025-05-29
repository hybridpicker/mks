# gallery/management/commands/optimize_gallery_images.py
"""
Management command to optimize existing gallery images.
This can be run to retroactively process images that were uploaded
before the optimization system was implemented.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from gallery.models import Photo, PhotoCategory
from gallery.image_utils import process_uploaded_image, get_image_info
import os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Optimize existing gallery images by creating missing thumbnails and lazy versions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--category',
            type=str,
            help='Process only images in a specific category (by title)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force reprocessing of all images, even if they already have thumbnails',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be processed without actually doing it',
        )

    def handle(self, *args, **options):
        category_filter = options.get('category')
        force = options.get('force', False)
        dry_run = options.get('dry_run', False)
        
        # Get photos to process
        photos = Photo.objects.all()
        
        if category_filter:
            try:
                category = PhotoCategory.objects.get(title=category_filter)
                photos = photos.filter(category=category)
                self.stdout.write(f"Processing category: {category.title}")
            except PhotoCategory.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Category '{category_filter}' not found"))
                return
        
        # Filter photos that need processing
        if not force:
            photos = photos.filter(image_thumbnail='', image_lazy='')
        
        total_photos = photos.count()
        self.stdout.write(f"Found {total_photos} photos to process")
        
        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN - No changes will be made"))
        
        processed = 0
        skipped = 0
        errors = 0
        
        for photo in photos:
            try:
                # Check if image file exists
                if not photo.image or not os.path.exists(photo.image.path):
                    self.stdout.write(self.style.WARNING(f"Skipping {photo.title}: Image file not found"))
                    skipped += 1
                    continue
                
                # Get image info
                info = get_image_info(photo.image)
                if info:
                    self.stdout.write(f"Processing: {photo.title} ({info['width']}x{info['height']}, {info['size_mb']}MB)")
                
                if dry_run:
                    processed += 1
                    continue
                
                # Process the image
                with transaction.atomic():
                    processed_images = process_uploaded_image(photo.image)
                    
                    # Update only if we got valid results
                    if processed_images['main']:
                        photo.image = processed_images['main']
                    
                    if processed_images['thumbnail'] and (force or not photo.image_thumbnail):
                        photo.image_thumbnail = processed_images['thumbnail']
                    
                    if processed_images['lazy'] and (force or not photo.image_lazy):
                        photo.image_lazy = processed_images['lazy']
                    
                    photo.save()
                    
                processed += 1
                self.stdout.write(self.style.SUCCESS(f"✓ Processed: {photo.title}"))
                
            except Exception as e:
                errors += 1
                self.stdout.write(self.style.ERROR(f"✗ Error processing {photo.title}: {str(e)}"))
                logger.error(f"Error processing photo {photo.id}: {str(e)}", exc_info=True)
        
        # Summary
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Processing complete!"))
        self.stdout.write(f"  Processed: {processed}")
        self.stdout.write(f"  Skipped: {skipped}")
        self.stdout.write(f"  Errors: {errors}")
        self.stdout.write(f"  Total: {total_photos}")
