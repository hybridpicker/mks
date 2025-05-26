from django.core.management.base import BaseCommand
from django.db import models
from blog.models import BlogPost
from PIL import Image

class Command(BaseCommand):
    help = 'Optimiert alle Blog-Banner-Bilder und setzt Focus-Points'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Zeigt nur an was gemacht würde, ohne Änderungen',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - Keine Änderungen werden gespeichert'))
        
        posts_with_images = BlogPost.objects.filter(
            image__isnull=False
        ).exclude(image='')
        
        self.stdout.write(f"Gefunden: {posts_with_images.count()} Blog-Posts mit Bildern")
        
        optimized_count = 0
        error_count = 0
        
        for post in posts_with_images:
            try:
                if post.image and hasattr(post.image, 'path'):
                    # Bildinfo vor Optimierung
                    with Image.open(post.image.path) as img:
                        old_width, old_height = img.size
                        old_ratio = old_width / old_height if old_height > 0 else 1
                    
                    self.stdout.write(f"Optimiere: {post.title}")
                    self.stdout.write(f"  Original: {old_width}x{old_height} (ratio: {old_ratio:.2f})")
                    
                    if not dry_run:
                        # Optimierung ausführen
                        post.optimize_banner_image()
                        
                        # Focus-Point setzen wenn nicht vorhanden
                        if post.image_focus_x is None:
                            post.image_focus_x = 0.5
                        if post.image_focus_y is None:
                            post.image_focus_y = 0.5
                        
                        post.save()
                        
                        self.stdout.write(
                            self.style.SUCCESS(f"  ✓ Optimiert: {post.image_width}x{post.image_height}")
                        )
                    else:
                        self.stdout.write("  → Würde optimiert werden")
                    
                    optimized_count += 1
                    
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f"Fehler bei {post.title}: {e}")
                )
        
        # Statistiken
        if not dry_run:
            landscape = BlogPost.objects.filter(
                image__isnull=False,
                image_width__gt=0,
                image_height__gt=0
            ).extra(where=["image_width::float / image_height::float > 1.2"]).count()
            
            portrait = BlogPost.objects.filter(
                image__isnull=False,
                image_width__gt=0,
                image_height__gt=0
            ).extra(where=["image_width::float / image_height::float < 0.8"]).count()
            
            square = BlogPost.objects.filter(
                image__isnull=False,
                image_width__gt=0,
                image_height__gt=0
            ).extra(where=["image_width::float / image_height::float BETWEEN 0.8 AND 1.2"]).count()
            
            self.stdout.write(self.style.SUCCESS(f"\nErgebnis:"))
            self.stdout.write(f"  Optimiert: {optimized_count}")
            self.stdout.write(f"  Fehler: {error_count}")
            self.stdout.write(f"  Querformat: {landscape}")
            self.stdout.write(f"  Hochformat: {portrait}")
            self.stdout.write(f"  Quadratisch: {square}")
        else:
            self.stdout.write(f"\nDry Run Ergebnis: {optimized_count} Bilder würden optimiert werden")
