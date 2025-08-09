accesslog = '-'
errorlog = '-'
loglevel = 'info'

# JSON access log with upstream response header X-Request-ID
access_log_format = (
    '{"time":"%(t)s","remote_addr":"%(h)s","request":"%(r)s",'
    '"status":%(s)s,"body_bytes":%(b)s,"referer":"%(f)s","user_agent":"%(a)s",'
    '"duration_us":%(D)s,"request_id":"%({X-Request-ID}o)s"}'
)

