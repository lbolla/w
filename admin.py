from google.appengine.api import users
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import webapp

from w import Handler


class Admin(Handler):

	def get(self):
		user = users.get_current_user()
		ctx = { 'subtitle': 'Admin',
				}
		self.render_tmpl('admin.html', ctx)


application = webapp.WSGIApplication([
	('/admin', Admin),
	],
	debug=True)

def main():
	run_wsgi_app(application)


if __name__ == "__main__":
	main()
