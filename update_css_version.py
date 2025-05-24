#!/usr/bin/env python3
"""MKS CSS Version Update Script - Simplified"""

import os
import re
import argparse
from pathlib import Path
import django

def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
    django.setup()

def get_project_version():
    try:
        from django.conf import settings
        return settings.VERSION if hasattr(settings, 'VERSION') else '1.0.0'
    except:
        return '1.0.0'

def find_mks_css_files(project_root):
    """Find only MKS-specific CSS files"""
    css_files = []
    include_paths = ['static/css', 'static/gallery/css']
    exclude_patterns = ['animate', 'tinymce', 'admin', 'ckeditor', 'vendor', '.min.css']
    
    for include_path in include_paths:
        full_path = project_root / include_path
        if full_path.exists():
            for css_file in full_path.rglob('*.css'):
                exclude = any(pattern in str(css_file) for pattern in exclude_patterns)
                if not exclude:
                    css_files.append(css_file)
    
    return css_files

def rename_css_file(css_file, version, dry_run=False):
    file_name = css_file.stem
    file_ext = css_file.suffix
    
    # Remove existing version
    file_name = re.sub(r'_v\d+\.\d+\.\d+$|\.\d+\.\d+\.\d+$', '', file_name)
    
    # Create new name: filename.version.css
    new_name = f"{file_name}.{version}{file_ext}"
    new_path = css_file.parent / new_name
    
    if not dry_run:
        css_file.rename(new_path)
        print(f"✅ {css_file.name} → {new_name}")
    else:
        print(f"🔄 {css_file.name} → {new_name}")
    
    return css_file.name, new_name
def update_template_references(template_file, css_changes, dry_run=False):
    """Update CSS references in template files"""
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        for old_name, new_name in css_changes.items():
            patterns = [
                rf'href=["\'][^"\']*{re.escape(old_name)}["\']',
                rf'{{% static ["\'][^"\']*{re.escape(old_name)}["\'] %}}',
            ]
            
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    content = re.sub(pattern, 
                                   lambda m: m.group(0).replace(old_name, new_name), 
                                   content, flags=re.IGNORECASE)
        
        if content != original_content:
            if not dry_run:
                with open(template_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"📝 Updated: {template_file}")
            return True
        return False
    except Exception as e:
        print(f"❌ Error updating {template_file}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Update MKS CSS files')
    parser.add_argument('--version', help='Version (default: from settings)')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes')
    args = parser.parse_args()
    
    project_root = Path('.').resolve()
    
    try:
        setup_django()
        version = args.version or get_project_version()
    except Exception as e:
        print(f"Warning: {e}")
        version = args.version or "1.0.0"
    
    print(f"🎯 MKS CSS Update to version {version}")
    print(f"{'🔄 DRY RUN MODE' if args.dry_run else '✅ LIVE MODE'}")
    
    css_files = find_mks_css_files(project_root)
    print(f"\n📁 Found {len(css_files)} MKS CSS files")
    
    css_changes = {}
    for css_file in css_files:
        old_name, new_name = rename_css_file(css_file, version, args.dry_run)
        css_changes[old_name] = new_name
    
    # Update templates
    template_files = list(Path('templates').rglob('*.html'))
    updated = sum(1 for tf in template_files if update_template_references(tf, css_changes, args.dry_run))
    
    print(f"\n🎉 Summary: {len(css_changes)} CSS files, {updated} templates")
    return 0

if __name__ == '__main__':
    exit(main())
