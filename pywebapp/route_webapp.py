import re

from pywebapp.root_webapp import RootWebApp

def route(route=None, **kwargs):
  def decorator(target):
    if not hasattr(target, 'routes'):
      target.routes = []
    target.routes.append(route)
    for arg in kwargs:
      setattr(target, arg, kwargs[arg])
    return target
  return decorator

def isbound(method):
  attr = None
  if hasattr(method, '__self__'):
    attr = method.__self__
  elif hasattr(method, 'im_self'):
    attr = method.im_self
  return attr is not None

DEFAULT_ROUTE_IDENTIFIER = ''

class RouteWebApp(RootWebApp):
  def __init__(self, *args, **kwargs):
    RootWebApp.__init__(self, *args, **kwargs)
    self.discover_routes()

  def add_route(self, regex, fn):
    self.routes[re.compile(regex) if len(regex) > 0 else ''] = fn

  def discover_routes(self):
    self.routes = {}
    for attr_str in dir(self):
      attr = getattr(self, attr_str)
      if not callable(attr) or\
         not hasattr(attr, 'routes'):
        continue
      routes = getattr(attr, 'routes')
      if not isinstance(routes, list):
        continue
      for regex in routes:
        self.add_route(regex, attr)

  def default_route(self, request, **kwargs):
    """called when no routes match the request
    """
    if DEFAULT_ROUTE_IDENTIFIER in self.routes:
      for result in self.route_call(request, DEFAULT_ROUTE_IDENTIFIER):
        yield result
    else:
      for result in RootWebApp.handle_request(self, request):
        yield result

  def route_target(self, route):
    # route_pattern -> method
    if route == None:
      return self.default_route
    else:
      return self.routes[route]

  def route_call(self, request, route, route_dict=None):
    # request, route, arg_dict -> response generator
    method = self.route_target(route)
    if route_dict == None:
      route_dict = {}
    if isbound(method):
      call = method(request, **route_dict)
    else:
      call = method(self, request, **route_dict)
    return call

  def handle_request(self, request):
    # request -> response generator
    route, args = self.route_lookup(request)
    for result in self.route_call(request, route, args):
      yield result

  def route_lookup(self, request):
    # request -> route_pattern, arg_dict
    for route in self.routes:
      if route == DEFAULT_ROUTE_IDENTIFIER:
        continue
      m = re.match(route, request.path)
      if m:
        match = True
        return route, m.groupdict()
    return None, None
