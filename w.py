import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

maintitle = 'Laura &amp; Lorenzo'

def render_tmpl(response, tmplname, ctx):
	path = os.path.join(os.path.dirname(__file__),
			'tmpl', tmplname)
	ctx['maintitle'] = maintitle
	response.out.write(template.render(path, ctx))


class Main(webapp.RequestHandler):
    def get(self):
		ctx = { 'subtitle': 'Main' }
		render_tmpl(self.response, 'main.html', ctx)


class Info(webapp.RequestHandler):
    def get(self):
		render_tmpl(self.response, 'info.html', {})


class Japan(webapp.RequestHandler):
    def get(self):
		render_tmpl(self.response, 'japan.html', {})


class Home(webapp.RequestHandler):
    def get(self):
		render_tmpl(self.response, 'home.html', {})


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
