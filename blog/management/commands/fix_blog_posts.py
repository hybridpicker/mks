from django.core.management.base import BaseCommand
from django.db import transaction
from blog.models import BlogPost
from django.utils.text import slugify
import uuid

class Command(BaseCommand):
    help = 'Fix common blog post issues like missing slugs, meta fields, etc.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            dest='dry_run',
            help='Show what would be fixed without making changes',
        )
        parser.add_argument(
            '--fix-slugs',
            action='store_true',
            dest='fix_slugs',
            help='Fix missing or duplicate slugs',
        )
        parser.add_argument(
            '--fix-meta',
            action='store_true',
            dest='fix_meta',
            help='Fix missing meta titles and descriptions',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        fix_slugs = options['fix_slugs']
        fix_meta = options['fix_meta']
        
        if not (fix_slugs or fix_meta):
            # If no specific fix is requested, do everything
            fix_slugs = True
            fix_meta = True

        self.stdout.write(
            self.style.SUCCESS(f'Starting blog post fix {"(DRY RUN)" if dry_run else ""}')
        )

        if fix_slugs:
            self.fix_blog_slugs(dry_run)
            
        if fix_meta:
            self.fix_meta_fields(dry_run)

        self.stdout.write(
            self.style.SUCCESS('Blog post fix completed!')
        )

    def fix_blog_slugs(self, dry_run=False):
        """Fix missing or duplicate slugs"""
        self.stdout.write('Checking blog post slugs...')
        
        # Find posts with missing slugs
        posts_without_slugs = BlogPost.objects.filter(slug__isnull=True) | BlogPost.objects.filter(slug='')
        
        self.stdout.write(f'Found {posts_without_slugs.count()} posts without slugs')
        
        for post in posts_without_slugs:
            new_slug = self.generate_unique_slug(post.title, post.pk)
            self.stdout.write(f'Post "{post.title}" -> slug: "{new_slug}"')
            
            if not dry_run:
                post.slug = new_slug
                post.save(update_fields=['slug'])

        # Find duplicate slugs
        self.check_duplicate_slugs(dry_run)

    def check_duplicate_slugs(self, dry_run=False):
        """Check and fix duplicate slugs"""
        from django.db.models import Count
        
        duplicate_slugs = (BlogPost.objects
                          .values('slug')
                          .annotate(count=Count('slug'))
                          .filter(count__gt=1))
        
        if duplicate_slugs:
            self.stdout.write(f'Found {len(duplicate_slugs)} duplicate slugs')
            
            for slug_info in duplicate_slugs:
                slug = slug_info['slug']
                posts = BlogPost.objects.filter(slug=slug).order_by('created_at')
                
                # Keep the first post's slug, fix the others
                for i, post in enumerate(posts[1:], start=1):
                    new_slug = f"{slug}-{i}"
                    
                    # Make sure this new slug is also unique
                    while BlogPost.objects.filter(slug=new_slug).exists():
                        new_slug = f"{slug}-{i}-{uuid.uuid4().hex[:4]}"
                    
                    self.stdout.write(f'Fixing duplicate: "{post.title}" -> "{new_slug}"')
                    
                    if not dry_run:
                        post.slug = new_slug
                        post.save(update_fields=['slug'])
        else:
            self.stdout.write('No duplicate slugs found')

    def fix_meta_fields(self, dry_run=False):
        """Fix missing meta titles and descriptions"""
        self.stdout.write('Checking meta fields...')
        
        # Fix missing meta titles
        posts_without_meta_title = BlogPost.objects.filter(meta_title__isnull=True) | BlogPost.objects.filter(meta_title='')
        
        self.stdout.write(f'Found {posts_without_meta_title.count()} posts without meta titles')
        
        for post in posts_without_meta_title:
            meta_title = post.title[:60] if post.title else f"Blog Post {post.pk}"
            self.stdout.write(f'Setting meta title for "{post.title}": "{meta_title}"')
            
            if not dry_run:
                post.meta_title = meta_title
                post.save(update_fields=['meta_title'])

        # Fix missing meta descriptions
        posts_without_meta_desc = BlogPost.objects.filter(meta_description__isnull=True) | BlogPost.objects.filter(meta_description='')
        
        self.stdout.write(f'Found {posts_without_meta_desc.count()} posts without meta descriptions')
        
        for post in posts_without_meta_desc:
            if post.lead_paragraph:
                meta_desc = post.lead_paragraph[:160]
            else:
                meta_desc = f"Blog post about {post.title}"[:160]
                
            self.stdout.write(f'Setting meta description for "{post.title}": "{meta_desc[:50]}..."')
            
            if not dry_run:
                post.meta_description = meta_desc
                post.save(update_fields=['meta_description'])

    def generate_unique_slug(self, title, exclude_pk=None):
        """Generate a unique slug for a title"""
        if not title:
            base_slug = f"blog-post-{uuid.uuid4().hex[:8]}"
        else:
            base_slug = slugify(title)
            if not base_slug:
                base_slug = f"blog-post-{uuid.uuid4().hex[:8]}"
        
        slug = base_slug
        counter = 1
        
        while True:
            qs = BlogPost.objects.filter(slug=slug)
            if exclude_pk:
                qs = qs.exclude(pk=exclude_pk)
            
            if not qs.exists():
                break
                
            slug = f"{base_slug}-{counter}"
            counter += 1
            
            # Prevent infinite loops
            if counter > 1000:
                slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
                break
        
        return slug
