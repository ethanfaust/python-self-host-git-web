import base64
import json

from pywebapp.route_webapp import RouteWebApp, route
from pywebapp.root_webapp import RootWebApp
from pywebapp import http_helper
from secure_webapp import SecureWebApp

def random_bytes(n):
  with open('/dev/urandom', 'rb') as f:
    return f.read(n)

class TestApp(SecureWebApp):
  @route('', requires_authentication=False)
  def not_found(self, request):
    request.response.send(status_code=http_helper.status['NOT_FOUND'], content_type='application/json')
    yield json.dumps({
      'status_code': http_helper.status['NOT_FOUND']
      })

  @route(r'^/info', requires_authentication=False)
  def info(self, request):
    for item in RootWebApp.info(self, request):
      yield item

  @route(r'^/verify', requires_authentication=False)
  def verify(self, request):
    request.response.send(content_type='application/json')
    result = {
      'authenticated': 'SSL_CLIENT_S_DN_CN' in request.env,
    }

    if 'SSL_CLIENT_S_DN_CN' in request.env:
      result.update({
        'username': request.env['SSL_CLIENT_S_DN_CN'],
        'device': request.env['SSL_CLIENT_S_DN_OU'],
        })
    yield json.dumps(result)

  @route(r'^/test/(?P<id>[0-9]+)$')
  @route(r'^/foo/(?P<id>[a-z]+)$')
  def test(self, request, id):
    request.response.send(content_type='application/json')
    yield json.dumps({
      'id': id
      })

  @route(r'^/random/(?P<num_bytes>[0-9]+)$')
  def random(self, request, num_bytes):
    num_bytes = int(num_bytes)
    if num_bytes < 1:
      num_bytes = 1
    if num_bytes > 8192:
      num_bytes = 8192
    request.response.send(content_type='application/json')
    yield json.dumps({
      'num_bytes': num_bytes,
      'bytes': base64.b64encode(random_bytes(num_bytes)).decode('utf-8')
      })
