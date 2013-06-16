import webapp2
import os
import logging

class PrintEnvironmentHandler(webapp2.RequestHandler):
    def get(self):
        for name in os.environ.keys():
            self.response.out.write("%s = %s<br />\n" % (name, os.environ[name]))

app = webapp2.WSGIApplication([
    ('/', PrintEnvironmentHandler),
], debug=True)