#!/usr/bin/env python  
"""
FINAL DEBUG: Monitor real browser form submission
"""

import os
import sys
import time
import threading
from queue import Queue

project_root = '/Users/lukasschonsgibl/Coding/Django/mks'
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
django.setup()

from blog.models import BlogPost

def monitor_database_changes():
    """Monitor database for new blog posts"""
    print("🔍 Monitoring database for new blog posts...")
    print("📊 Current blog posts in database:")
    
    initial_posts = list(BlogPost.objects.all().values('id', 'title', 'created_at'))
    for post in initial_posts:
        print(f"  ID: {post['id']} - {post['title']} - {post['created_at']}")
    
    print(f"\nTotal: {len(initial_posts)} posts")
    print("\n" + "="*60)
    print("🚀 NOW GO TO YOUR BROWSER AND TRY TO CREATE A BLOG POST!")
    print("   URL: http://localhost:8000/blogedit/new")
    print("="*60)
    
    last_count = len(initial_posts)
    
    while True:
        try:
            current_posts = BlogPost.objects.all()
            current_count = current_posts.count()
            
            if current_count != last_count:
                print(f"\n🎉 DATABASE CHANGE DETECTED!")
                print(f"   Posts count changed: {last_count} → {current_count}")
                
                if current_count > last_count:
                    # New posts added
                    new_posts = current_posts.exclude(
                        id__in=[p['id'] for p in initial_posts]
                    ).order_by('-id')[:5]
                    
                    print("📝 NEW BLOG POSTS:")
                    for post in new_posts:
                        print(f"   ✅ ID: {post.id}")
                        print(f"      Title: {post.title}")
                        print(f"      Slug: {post.slug}")  
                        print(f"      Published: {post.published}")
                        print(f"      Image: {post.image.name if post.image else 'None'}")
                        print(f"      Created: {post.created_at}")
                        print()
                
                # Update tracking
                last_count = current_count
                initial_posts = list(current_posts.values('id', 'title', 'created_at'))
            
            time.sleep(1)  # Check every second
            
        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped by user")
            break
        except Exception as e:
            print(f"\n❌ Error monitoring database: {e}")
            time.sleep(5)

def monitor_logs():
    """Monitor Django logs"""
    log_file = os.path.join(project_root, 'logs', 'django.log')
    
    print(f"📋 Monitoring Django logs: {log_file}")
    
    if not os.path.exists(log_file):
        print("⚠️  Log file doesn't exist yet, creating...")
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, 'w') as f:
            f.write('')
    
    try:
        with open(log_file, 'r') as f:
            # Go to end of file
            f.seek(0, 2)
            
            while True:
                line = f.readline()
                if line:
                    # Print new log lines with timestamp
                    timestamp = time.strftime('%H:%M:%S')
                    print(f"[{timestamp}] {line.strip()}")
                else:
                    time.sleep(0.1)
                    
    except KeyboardInterrupt:
        print("\n👋 Log monitoring stopped")
    except Exception as e:
        print(f"\n❌ Error monitoring logs: {e}")

def main():
    print("🔧 FINAL BLOG DEBUG - LIVE MONITORING")
    print("=" * 60)
    print("This script will monitor:")
    print("1. 📊 Database changes (new blog posts)")
    print("2. 📋 Django logs (errors and info)")  
    print("3. 🕒 Real-time updates")
    print("=" * 60)
    
    # Start monitoring threads
    db_thread = threading.Thread(target=monitor_database_changes, daemon=True)
    log_thread = threading.Thread(target=monitor_logs, daemon=True)
    
    db_thread.start()
    log_thread.start()
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Monitoring stopped by user")
        print("=" * 60)
        
        # Final summary
        final_count = BlogPost.objects.count()
        print(f"📊 Final blog posts count: {final_count}")
        
        recent_posts = BlogPost.objects.order_by('-id')[:3]
        if recent_posts:
            print("🕒 Most recent posts:")
            for post in recent_posts:
                print(f"   - {post.title} (ID: {post.id}, Created: {post.created_at})")
        
        print("\n💡 If no new posts were created, check:")
        print("   1. Form validation errors in browser console")
        print("   2. JavaScript errors preventing form submission")  
        print("   3. Content field length (must be >10 characters)")
        print("   4. Network tab in browser dev tools")
        print("   5. CSRF token issues")

if __name__ == "__main__":
    main()
