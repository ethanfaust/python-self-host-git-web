import base64
import json

from pywebapp.route_webapp import RouteWebApp, route
from pywebapp.root_webapp import RootWebApp
from pywebapp import http_helper

from githost import actions

class PyGitWeb(RouteWebApp):
  @route('')
  def not_found(self, request):
    request.response.send(status_code=http_helper.status['NOT_FOUND'], content_type='application/json')
    yield json.dumps({
      'status_code': http_helper.status['NOT_FOUND']
      })

  @route('^/$')
  def main(self, request):
    request.response.send(content_type='application/json')
    yield json.dumps({
      'repositories': list(actions.iter_repos())
      })

  @route(r'^/create/(?P<repo_name>[a-z_0-9\-]+)$')
  def create(self, request, repo_name):
    result, error = actions.create_repo(repo_name)
    if result:
      request.response.send(content_type='application/json')
      yield json.dumps({
        'status': 'ok',
        })
    else:
      request.response.send(status_code=http_helper.status['BAD_REQUEST'], content_type='application/json')
      yield json.dumps({
        'status': 'bad_request',
        'error': error,
        })

  @route(r'^/info')
  def info(self, request):
    for item in RootWebApp.info(self, request):
      yield item
