# Gunicorn configuration file for MKS
# Place this in your project root as gunicorn_config.py

import multiprocessing

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# Timeout settings - IMPORTANT for PDF generation
timeout = 120  # Increased from default 30s for PDF generation
graceful_timeout = 120
keepalive = 5

# Logging
accesslog = '/var/log/gunicorn/access.log'
errorlog = '/var/log/gunicorn/error.log'
loglevel = 'info'

# Process naming
proc_name = 'mks_gunicorn'

# Server mechanics
daemon = False
pidfile = '/var/run/gunicorn.pid'
user = None
group = None
tmp_upload_dir = None

# SSL/Security
keyfile = None
certfile = None

# Debugging
reload = False
reload_engine = 'auto'
reload_extra_files = []

# Pre-request hook to handle large requests
def pre_request(worker, req):
    worker.log.debug("Worker handling request %s", req.path)

# Post-request hook
def post_request(worker, req, environ, resp):
    worker.log.debug("Worker finished request %s", req.path)

# Worker timeout handling
def worker_int(worker):
    worker.log.info("Worker received INT or QUIT signal")

# Memory limit per worker (optional)
# limit_request_line = 4094
# limit_request_fields = 100
# limit_request_field_size = 8190
