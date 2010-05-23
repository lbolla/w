import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import mail, users
from google.appengine.ext.webapp import template

import validate


EXC = None

def set_exc(e=None):
	global EXC
	EXC = e


class Handler(webapp.RequestHandler):

	maintitle = 'Laura &amp; Lorenzo'

	def initialize(self, *args, **kwargs):
		set_exc()
		super(Handler, self).initialize(*args, **kwargs)
		self.user = users.get_current_user()

	def render_tmpl(self, tmplname, ctx):
		path = os.path.join(os.path.dirname(__file__),
				'tmpl', tmplname)
		ctx['maintitle'] = self.maintitle
		ctx['EXC'] = EXC
		ctx['user'] = self.user
		ctx['logout_url'] = users.create_logout_url('/')
		self.response.out.write(template.render(path, ctx))


class Main(Handler):

	def get(self):
		ctx = {}
		self.render_tmpl('main.html', ctx)


class Info(Handler):

	def get(self):
		ctx = { 'subtitle': 'Info' }
		self.render_tmpl('info.html', ctx)


class Japan(Handler):

	# TODO
	# only allow a limited numbers of submits per IP

	def initialize(self, *args, **kwargs):
		set_exc()
		super(Japan, self).initialize(*args, **kwargs)

	def get(self):
		ctx = { 'subtitle': 'Japan' }
		self.render_tmpl('japan.html', ctx)

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
		self.render_tmpl('home.html', ctx)


application = webapp.WSGIApplication([
	('/', Main),
	('/info', Info),
	('/japan', Japan),
	('/home', Home),
	],
	debug=True)


def main():
	run_wsgi_app(application)


if __name__ == "__main__":
	main()
