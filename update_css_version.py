#!/usr/bin/env python3
"""
CSS Version Update Script for Django Project
============================================

This script updates all CSS files and their references in a Django project
to a specific version number.

Usage:
    python update_css_version.py --version 3.0.0

Features:
- Detects current Django version
- Renames all CSS files to include version number (e.g., mks.css -> mks.3.0.0.css)
- Updates all references in HTML templates, Django templates, and static files
- Creates backup of original files
- Supports dry-run mode for testing

Author: MKS Development Team
"""

import os
import re
import shutil
import argparse
import json
from pathlib import Path
from datetime import datetime
import django


def setup_django():
    """Setup Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
    django.setup()


def get_django_version():
    """Get current Django version"""
    try:
        import django
        return django.VERSION[:3]  # Major.Minor.Patch
    except ImportError:
        return None


def find_css_files(project_root):
    """Find all CSS files in the project"""
    css_files = []
    static_dirs = [
        'static',
        'staticfiles',
        'static_cdn',
    ]
    
    for static_dir in static_dirs:
        static_path = project_root / static_dir
        if static_path.exists():
            for css_file in static_path.rglob('*.css'):
                css_files.append(css_file)
    
    # Also check app-specific static directories
    for app_dir in project_root.iterdir():
        if app_dir.is_dir():
            app_static = app_dir / 'static'
            if app_static.exists():
                for css_file in app_static.rglob('*.css'):
                    css_files.append(css_file)
    
    return css_files


def find_template_files(project_root):
    """Find all template files that might reference CSS"""
    template_files = []
    template_extensions = ['.html', '.htm', '.django', '.jinja2']
    
    # Main templates directory
    templates_dir = project_root / 'templates'
    if templates_dir.exists():
        for ext in template_extensions:
            template_files.extend(templates_dir.rglob(f'*{ext}'))
    
    # App-specific template directories
    for app_dir in project_root.iterdir():
        if app_dir.is_dir():
            app_templates = app_dir / 'templates'
            if app_templates.exists():
                for ext in template_extensions:
                    template_files.extend(app_templates.rglob(f'*{ext}'))
    
    return template_files


def create_backup(file_path, backup_dir):
    """Create backup of a file"""
    backup_dir.mkdir(parents=True, exist_ok=True)
    relative_path = file_path.relative_to(file_path.parts[0])
    backup_path = backup_dir / relative_path
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(file_path, backup_path)
    return backup_path


def rename_css_file(css_file, version, dry_run=False):
    """Rename CSS file to include version number"""
    file_name = css_file.stem
    file_ext = css_file.suffix
    
    # Check if already versioned
    version_pattern = r'\.\d+\.\d+\.\d+$'
    if re.search(version_pattern, file_name):
        # Remove existing version
        file_name = re.sub(version_pattern, '', file_name)
    
    new_name = f"{file_name}.{version}{file_ext}"
    new_path = css_file.parent / new_name
    
    if not dry_run:
        css_file.rename(new_path)
        print(f"Renamed: {css_file} -> {new_path}")
    else:
        print(f"Would rename: {css_file} -> {new_path}")
    
    return css_file.name, new_name


def update_template_references(template_file, css_changes, version, dry_run=False):
    """Update CSS references in template files"""
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = []
        
        for old_name, new_name in css_changes.items():
            # Patterns to match CSS references
            patterns = [
                # Standard link tags
                rf'<link[^>]*href=["\'][^"\']*{re.escape(old_name)}["\'][^>]*>',
                # Static template tags
                rf'{{% static ["\'][^"\']*{re.escape(old_name)}["\'] %}}',
                # Load static references
                rf'static/[^"\']*{re.escape(old_name)}',
                # Direct CSS references
                rf'["\'][^"\']*{re.escape(old_name)}["\']',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    content = re.sub(pattern, lambda m: m.group(0).replace(old_name, new_name), content, flags=re.IGNORECASE)
                    changes_made.extend(matches)
        
        if content != original_content:
            if not dry_run:
                with open(template_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated template: {template_file}")
            else:
                print(f"Would update template: {template_file}")
            return True
        
        return False
        
    except Exception as e:
        print(f"Error updating {template_file}: {e}")
        return False


def create_version_info(project_root, version, css_changes):
    """Create version info file"""
    version_info = {
        'version': version,
        'updated_at': datetime.now().isoformat(),
        'django_version': '.'.join(map(str, get_django_version())) if get_django_version() else 'unknown',
        'css_files_updated': len(css_changes),
        'css_changes': css_changes
    }
    
    version_file = project_root / f'css_version_{version}.json'
    with open(version_file, 'w', encoding='utf-8') as f:
        json.dump(version_info, f, indent=2, ensure_ascii=False)
    
    print(f"Version info saved to: {version_file}")


def main():
    parser = argparse.ArgumentParser(description='Update CSS files to specific version')
    parser.add_argument('--version', required=True, help='Version number (e.g., 3.0.0)')
    parser.add_argument('--project-root', default='.', help='Django project root directory')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--backup', action='store_true', help='Create backup of original files')
    parser.add_argument('--force', action='store_true', help='Force update even if Django version mismatch')
    
    args = parser.parse_args()
    
    # Validate version format
    if not re.match(r'^\d+\.\d+\.\d+$', args.version):
        print("Error: Version must be in format X.Y.Z (e.g., 3.0.0)")
        return 1
    
    project_root = Path(args.project_root).resolve()
    
    if not project_root.exists():
        print(f"Error: Project root '{project_root}' does not exist")
        return 1
    
    print(f"CSS Version Update Script")
    print(f"========================")
    print(f"Project Root: {project_root}")
    print(f"Target Version: {args.version}")
    print(f"Dry Run: {args.dry_run}")
    print()
    
    # Setup Django
    try:
        os.chdir(project_root)
        setup_django()
        django_version = get_django_version()
        if django_version:
            django_version_str = '.'.join(map(str, django_version))
            print(f"Django Version: {django_version_str}")
            
            # Check if target version matches Django version
            if not args.force and args.version != django_version_str:
                print(f"Warning: Target version ({args.version}) doesn't match Django version ({django_version_str})")
                if not args.dry_run:
                    confirm = input("Continue anyway? (y/N): ")
                    if confirm.lower() != 'y':
                        print("Aborted.")
                        return 1
        else:
            print("Warning: Could not detect Django version")
    except Exception as e:
        print(f"Warning: Could not setup Django environment: {e}")
    
    print()
    
    # Find CSS files
    print("Finding CSS files...")
    css_files = find_css_files(project_root)
    print(f"Found {len(css_files)} CSS files")
    
    if not css_files:
        print("No CSS files found!")
        return 1
    
    # Create backup if requested
    backup_dir = None
    if args.backup and not args.dry_run:
        backup_dir = project_root / 'css_backup' / datetime.now().strftime('%Y%m%d_%H%M%S')
        print(f"Creating backup in: {backup_dir}")
    
    # Rename CSS files
    print("\nRenaming CSS files...")
    css_changes = {}
    
    for css_file in css_files:
        if args.backup and backup_dir:
            create_backup(css_file, backup_dir)
        
        old_name, new_name = rename_css_file(css_file, args.version, args.dry_run)
        css_changes[old_name] = new_name
    
    # Find and update template files
    print(f"\nFinding template files...")
    template_files = find_template_files(project_root)
    print(f"Found {len(template_files)} template files")
    
    print(f"\nUpdating template references...")
    updated_templates = 0
    
    for template_file in template_files:
        if args.backup and backup_dir:
            create_backup(template_file, backup_dir)
        
        if update_template_references(template_file, css_changes, args.version, args.dry_run):
            updated_templates += 1
    
    # Create version info
    if not args.dry_run:
        create_version_info(project_root, args.version, css_changes)
    
    print(f"\nSummary:")
    print(f"========")
    print(f"CSS files updated: {len(css_changes)}")
    print(f"Templates updated: {updated_templates}")
    
    if args.dry_run:
        print(f"\nThis was a dry run. No files were actually modified.")
        print(f"Run without --dry-run to apply changes.")
    else:
        print(f"\nCSS version update completed successfully!")
        if backup_dir:
            print(f"Backup created in: {backup_dir}")
    
    return 0


if __name__ == '__main__':
    exit(main())
