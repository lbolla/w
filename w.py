import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template


class Main(webapp.RequestHandler):
    def get(self):
		path = os.path.join(os.path.dirname(__file__), 
				'tmpl/index.html')
		ctx = {}
		self.response.out.write(template.render(path, ctx))


class Info(webapp.RequestHandler):
    def get(self):
		path = os.path.join(os.path.dirname(__file__), 
				'tmpl/info.html')
		ctx = {}
		self.response.out.write(template.render(path, ctx))


class Japan(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Sakura @csszengarden')


class Home(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Home')


application = webapp.WSGIApplication(
                                     [('/', Main),
                                      ('/info/', Info),
                                      ('/japan/', Japan),
                                      ('/home/', Home),
									],
                                     debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
