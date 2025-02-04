# gunicorn_config.py

# Server socket
bind = '0.0.0.0:5005'  # Address and port to bind

# Worker processes
workers = 4  # Number of worker processes for handling requests

# Worker class
worker_class = 'sync'  # The type of workers to use (sync, async, etc.)

# Logging
accesslog = '-'  # Log access requests to stdout
errorlog = '-'  # Log errors to stdout
loglevel = 'info'  # The granularity of log output

# Timeout
timeout = 120  # Workers silent for more than this many seconds are killed and restarted

# Preload application
preload_app = True  # Load application code before the worker processes are forked