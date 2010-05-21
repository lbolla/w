import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import mail

import validate


maintitle = 'Laura &amp; Lorenzo'
EXC = None


def render_tmpl(response, tmplname, ctx):
	path = os.path.join(os.path.dirname(__file__),
			'tmpl', tmplname)
	ctx['maintitle'] = maintitle
	ctx['EXC'] = EXC
	response.out.write(template.render(path, ctx))


def set_exc(e=None):
	global EXC
	EXC = e


class Handler(webapp.RequestHandler):
	def initialize(self, *args, **kwargs):
		set_exc()
		super(Handler, self).initialize(*args, **kwargs)


class Main(Handler):

	def get(self):
		ctx = {}
		render_tmpl(self.response, 'main.html', ctx)


class Info(Handler):

	def get(self):
		ctx = { 'subtitle': 'Info' }
		render_tmpl(self.response, 'info.html', ctx)


class Japan(Handler):

	# TODO
	# only allow a limited numbers of submits per IP

	def initialize(self, *args, **kwargs):
		set_exc()
		super(Japan, self).initialize(*args, **kwargs)

	def get(self):
		ctx = { 'subtitle': 'Japan' }
		render_tmpl(self.response, 'japan.html', ctx)

	def post(self):
		try:
			amount = self.request.get("amount")
			validate.validate_number(amount, minval=0)

			# for security reasons only mails from me are allowed
			to_addr = "lbolla@gmail.com"
			from_addr = "lbolla@gmail.com"
			sender = self.request.get("sender")
			subject = "Mail from %s" % sender
			body = self.request.get("body")
			mail.send_mail(from_addr, to_addr, subject, body)
		except Exception, e:
			set_exc(e)
		self.get()


class Home(Handler):

	def get(self):
		ctx = { 'subtitle': 'Home' }
		render_tmpl(self.response, 'home.html', ctx)


application = webapp.WSGIApplication(
									 [('/', Main),
									  ('/info', Info),
									  ('/japan', Japan),
									  ('/home', Home),
									],
									 debug=True)


def main():
	run_wsgi_app(application)


if __name__ == "__main__":
	main()
