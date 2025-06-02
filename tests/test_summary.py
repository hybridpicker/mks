#!/usr/bin/env python
"""
Test structure verification and summary script for MKS project.
"""

import os
import glob

def count_tests():
    """Count and categorize all test files."""
    
    test_base = 'tests'
    
    print("🧪 MKS Project Test Structure Summary")
    print("=" * 50)
    
    # Root tests
    root_tests = glob.glob(f"{test_base}/root_tests/test_*.py")
    print(f"\n📁 Root Tests ({len(root_tests)} files):")
    for test in root_tests:
        print(f"  - {os.path.basename(test)}")
    
    # App tests by directory
    app_test_dirs = glob.glob(f"{test_base}/app_tests/*/")
    app_test_count = 0
    
    print(f"\n📱 App Tests ({len(app_test_dirs)} apps):")
    for app_dir in sorted(app_test_dirs):
        app_name = os.path.basename(app_dir.rstrip('/'))
        app_tests = glob.glob(f"{app_dir}test_*.py") + glob.glob(f"{app_dir}tests.py")
        app_test_count += len(app_tests)
        print(f"  📂 {app_name} ({len(app_tests)} files)")
        for test in app_tests:
            print(f"    - {os.path.basename(test)}")
    
    # Main tests directory
    main_tests = [f for f in glob.glob(f"{test_base}/test_*.py") if not f.startswith(f"{test_base}/test_settings")]
    print(f"\n📋 Main Tests ({len(main_tests)} files):")
    for test in main_tests:
        print(f"  - {os.path.basename(test)}")
    
    # Test runners
    runners = glob.glob(f"{test_base}/run_*.py")
    print(f"\n🏃 Test Runners ({len(runners)} files):")
    for runner in runners:
        print(f"  - {os.path.basename(runner)}")
    
    # Summary
    total_tests = len(root_tests) + app_test_count + len(main_tests)
    print(f"\n📊 Summary:")
    print(f"  Total test files: {total_tests}")
    print(f"  Root tests: {len(root_tests)}")
    print(f"  App tests: {app_test_count}")
    print(f"  Main tests: {len(main_tests)}")
    print(f"  Test runners: {len(runners)}")
    print(f"  Total apps with tests: {len(app_test_dirs)}")
    
    print(f"\n🔧 Git Hooks:")
    hooks_dir = ".git/hooks"
    if os.path.exists(f"{hooks_dir}/pre-commit"):
        print("  ✅ pre-commit hook configured")
    if os.path.exists(f"{hooks_dir}/pre-push"):
        print("  ✅ pre-push hook configured")
    
    print(f"\n🚀 Usage:")
    print("  Run all tests: python manage.py test tests")
    print("  Run root tests: python manage.py test tests.root_tests")
    print("  Run app tests: python manage.py test tests.app_tests")
    print("  Run specific app: python manage.py test tests.app_tests.gallery")

if __name__ == '__main__':
    count_tests()
