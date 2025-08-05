# Gunicorn configuration file for Render deployment
import os

# Server socket - CRITICAL for 502 Bad Gateway fix
bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"
backlog = 2048

# Worker processes - optimized for Render
workers = 1  # Reduced for memory constraints
worker_class = 'sync'
worker_connections = 1000
timeout = 120  # Increased timeout as per Render docs
keepalive = 5

# Memory management
max_requests = 1000
max_requests_jitter = 50
preload_app = False  # Disable preloading to reduce memory usage

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Process naming
proc_name = 'resume-reviewer'

# Server mechanics
daemon = False
pidfile = None
user = None
group = None
tmp_upload_dir = None

# SSL (not needed for Render)
keyfile = None
certfile = None

# Additional settings for Render
worker_tmp_dir = '/dev/shm'  # Use shared memory for temp files 