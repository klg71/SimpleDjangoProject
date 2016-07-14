"""
WSGI config for simple_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys
import io

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simple_project.settings")

application = get_wsgi_application()

def call_application(environ,postdata='',header=''):
    inputStream=io.BytesIO()
    
    environ['wsgi.input'] = inputStream
    environ['wsgi.errros'] = sys.stderr
    environ['wsgi.version']= (1,0)
    print(header)
    if postdata:
        print(postdata)
        print(sys.version)
        environ['wsgi.input']=io.BytesIO(postdata.encode('utf-8'))
        environ['CONTENT_LENGTH']=str(len(postdata.encode('utf-8')))
        environ['CONTENT_TYPE']='application/x-wwww-form-urlencoded'
    if 'Cookie' in header:
        environ['HTTP_COOKIE']=header['Cookie']
    if 'User-Agent' in header:
        environ['HTTP_USER_AGENT']=header['User-Agent']
    if 'Host' in header:
        environ['HTTP_HOST']=header['Host']
    if 'Content-Type' in header:
        environ['CONTENT_TYPE']=header['Content-Type']
    if 'Accept' in header:
        environ['HTTP_ACCEPT'] = header['Accept']
    if 'Accept-Encoding' in header:
        environ['HTTP_ACCEPT_ENCODING'] =header['Accept-Encoding']

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
