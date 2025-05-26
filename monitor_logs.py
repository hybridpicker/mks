#!/usr/bin/env python
"""
Real-Time Django Log Monitor
"""

import os
import sys
import time
import threading

project_root = '/Users/lukasschonsgibl/Coding/Django/mks'
log_file = os.path.join(project_root, 'logs', 'django.log')

def monitor_logs():
    """Monitor Django logs in real-time"""
    print(f"Monitoring Django logs: {log_file}")
    print("=" * 50)
    print("Now try to create a blog post with image in your browser...")
    print("Go to: http://localhost:8000/blogedit/new")
    print("=" * 50)
    
    if not os.path.exists(log_file):
        print("Log file doesn't exist yet. Creating...")
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, 'w') as f:
            f.write('')
    
    # Follow the log file
    with open(log_file, 'r') as f:
        # Go to end of file
        f.seek(0, 2)
        
        while True:
            line = f.readline()
            if line:
                # Print new log lines
                print(line.strip())
            else:
                time.sleep(0.1)

if __name__ == "__main__":
    try:
        monitor_logs()
    except KeyboardInterrupt:
        print("\nLog monitoring stopped.")
