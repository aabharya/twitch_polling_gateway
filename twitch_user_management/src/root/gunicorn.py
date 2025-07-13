wsgi_app = 'root.wsgi'
bind = ':8000'
timeout = 120
enable_stdio_inheritance = True
errorlog = '-'
accesslog = '-'
capture_output = True
max_requests = 1000
max_requests_jitter = 100
threads = 4
loglevel = 'info'
access_log_format = '[%(h)s] [%(u)s] %(t)s [%(r)s] [%(s)s] [referer=%(f)s] [request_time=%(L)s] [%(a)s]'


def when_ready(server):
    server.log.info('User Management server is ready. Spawning workers')


def post_fork(server, worker):
    server.log.info('User Management worker spawned (pid: %s)', worker.pid)
