"""
WSGI config for simple_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simple_project.settings")

application = get_wsgi_application()

def call_application(environ):
    environ['wsgi.input'] = sys.stdin
    environ['wsgi.errros'] = sys.stderr
    environ['wsgi.version']= (1,0)
    headers_set = []
    
    def write(data):
        #sys.stdout.write(data)
        sys.stdout.flush()

    def start_response(status,response_headers,exc_info=None):
        headers_set[:]=[status,response_headers]
        return write

    result=application(environ,start_response)
    stringresult=''.join([x.decode('utf-8') for x in result])
    try:
        for data in result:
            if data:
                write(data.decode('utf-8'))
    finally:
        if hasattr(result,'close'):
            result.close()

    return {'body':stringresult,'headers':headers_set[1:],'status':headers_set[0]}
