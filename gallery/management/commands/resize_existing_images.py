from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from gallery.models import Photo
from gallery.image_utils import process_uploaded_image, get_image_info
from django.core.files import File
import os
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Resize existing images in the gallery that are too large'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be processed without actually doing it',
        )
        parser.add_argument(
            '--min-size',
            type=int,
            default=3,
            help='Minimum file size in MB to process (default: 3)',
        )
        parser.add_argument(
            '--category',
            type=str,
            help='Process only photos from specific category',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        min_size_bytes = options['min_size'] * 1024 * 1024
        category_filter = options['category']

        self.stdout.write(
            self.style.SUCCESS(
                f"{'DRY RUN: ' if dry_run else ''}Processing images larger than {options['min_size']}MB"
            )
        )

        # Get photos to process
        photos = Photo.objects.all()
        if category_filter:
            photos = photos.filter(category__title__icontains=category_filter)

        processed_count = 0
        error_count = 0
        skipped_count = 0

        for photo in photos:
            try:
                # Check if image file exists
                image_path = os.path.join(settings.MEDIA_ROOT, photo.image.name)
                if not os.path.exists(image_path):
                    self.stdout.write(
                        self.style.WARNING(f"Skipping {photo.title}: Image file not found")
                    )
                    skipped_count += 1
                    continue

                # Check file size
                file_size = os.path.getsize(image_path)
                if file_size < min_size_bytes:
                    continue

                # Get image info
                with open(image_path, 'rb') as img_file:
                    image_info = get_image_info(img_file)

                if not image_info:
                    self.stdout.write(
                        self.style.WARNING(f"Skipping {photo.title}: Could not read image info")
                    )
                    skipped_count += 1
                    continue

                self.stdout.write(
                    f"Processing: {photo.title} "
                    f"({image_info['width']}x{image_info['height']}, "
                    f"{image_info['size_mb']}MB)"
                )

                if not dry_run:
                    # Process the image
                    with open(image_path, 'rb') as img_file:
                        # Create a temporary uploaded file-like object
                        django_file = File(img_file)
                        django_file.name = os.path.basename(image_path)
                        
                        processed_images = process_uploaded_image(django_file)

                        # Update the photo with processed images
                        if processed_images['main']:
                            photo.image = processed_images['main']

                        if processed_images['thumbnail']:
                            photo.image_thumbnail = processed_images['thumbnail']

                        if processed_images['lazy']:
                            photo.image_lazy = processed_images['lazy']

                        photo.save()

                        # Log the result
                        new_size = photo.image.size / (1024 * 1024)
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"  → Resized to {new_size:.2f}MB "
                                f"(saved {image_info['size_mb'] - new_size:.2f}MB)"
                            )
                        )

                processed_count += 1

            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f"Error processing {photo.title}: {str(e)}")
                )

        # Summary
        self.stdout.write("\n" + "="*50)
        self.stdout.write(f"{'DRY RUN ' if dry_run else ''}SUMMARY:")
        self.stdout.write(f"  Processed: {processed_count}")
        self.stdout.write(f"  Errors: {error_count}")
        self.stdout.write(f"  Skipped: {skipped_count}")
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING("This was a dry run. Use without --dry-run to actually process images.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("Image processing completed!")
            )
