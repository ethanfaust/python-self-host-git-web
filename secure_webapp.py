from pywebapp.route_webapp import RouteWebApp
from pywebapp import http_helper

AUTHENTICATION_ATTR = 'requires_authentication'

class SecureWebApp(RouteWebApp):
  def is_authenticated(self, request):
    # TODO: override this for stronger authentication / guarantees
    return 'REMOTE_USER' in request.env

  def unauthenticated_request_handler(self, request):
    status = 'UNAUTHORIZED'
    request.response.send(status_code=http_helper.status[status])
    yield 'HTTP {code} {text}'.format(code=http_helper.status[status], text=status)

  def handle_request(self, request):
    route, args = self.route_lookup(request)
    method = self.route_target(route)
    if (hasattr(method, AUTHENTICATION_ATTR) and not getattr(method, AUTHENTICATION_ATTR))\
      or self.is_authenticated(request):
      for result in self.route_call(request, route, args):
        yield result
    else:
      for result in self.unauthenticated_request_handler(request):
        yield result
