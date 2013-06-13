import webapp2
import os

class PrintEnvironmentHandler(webapp2.RequestHandler):
    def get(self):
        for name in os.environ.keys():
            self.response.out.write("%s = %s<br />\n" % (name, os.environ[name]))

application = webapp2.WSGIApplication([
    ('/', PrintEnvironmentHandler),
], debug=True)