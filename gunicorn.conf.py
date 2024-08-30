bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
threads = 2 
timeout = 120
keepalive = 5
loglevel = "info"
wsgi_app = "wsgi:app"