#!/usr/bin/env python
"""
CircleCI Compatibility Test
"""

import os
import sys
import tempfile

# Add the project root to the Python path
project_root = '/Users/lukasschonsgibl/Coding/Django/mks'
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def test_logging_config():
    """Test if logging configuration works without logs directory"""
    print("Testing logging configuration...")
    
    # Temporarily move logs directory if it exists
    logs_dir = os.path.join(project_root, 'logs')
    temp_logs_dir = None
    
    if os.path.exists(logs_dir):
        temp_logs_dir = logs_dir + '_temp'
        os.rename(logs_dir, temp_logs_dir)
    
    try:
        # Test Django setup without logs directory
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
        import django
        django.setup()
        
        print("✓ Django setup successful without logs directory")
        
        # Test that logging works
        import logging
        logger = logging.getLogger('blog')
        logger.info("Test log message")
        
        print("✓ Logging works correctly")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
        
    finally:
        # Restore logs directory if it existed
        if temp_logs_dir and os.path.exists(temp_logs_dir):
            if os.path.exists(logs_dir):
                # Remove the newly created logs dir
                import shutil
                shutil.rmtree(logs_dir)
            os.rename(temp_logs_dir, logs_dir)

def test_basic_django_commands():
    """Test basic Django commands"""
    print("\nTesting Django commands...")
    
    try:
        import django
        from django.core.management import execute_from_command_line
        
        # Test check command
        execute_from_command_line(['manage.py', 'check'])
        print("✓ Django check command successful")
        
        return True
        
    except Exception as e:
        print(f"✗ Django command error: {e}")
        return False

def main():
    print("CIRCLECI COMPATIBILITY TEST")
    print("=" * 40)
    
    tests = [
        ("Logging Configuration", test_logging_config),
        ("Django Commands", test_basic_django_commands),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 40)
    print("TEST RESULTS:")
    print("=" * 40)
    
    all_passed = True
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n✅ ALL TESTS PASSED!")
        print("The application should work correctly on CircleCI.")
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("There may be issues on CircleCI.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
