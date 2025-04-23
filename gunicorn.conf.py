# pylint: disable=invalid-name

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = 6
worker_class = "gevent"
worker_connections = 1000
timeout = 30
keepalive = 2
reload = True

# Logging
loglevel = "debug"
accesslog = "./access.log"
errorlog = "./error.log"
