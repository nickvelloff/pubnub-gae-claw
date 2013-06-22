import webapp2
import logging

import config.globals

from model.ClawUser import ClawUser
import hashlib
import time
from datetime import datetime
import logging

# from google.appengine.api.backends.backends import get_url, get_backend, get_hostname
# from google.appengine.api.urlfetch import fetch

class RequestClawAccess(webapp2.RequestHandler):
    def get(self):
                        
        allUsers = ClawUser().all()
        numusers = allUsers.count() #max 1000, not an issue in our case
        
        if numusers < config.globals.max_connections:
            
            hasher = hashlib.sha1()
            hasher.update(str(time.time()))
            channelId = hasher.hexdigest()[:20]
        
            cu = ClawUser()
            cu.channel = channelId
            cu.timestamp = datetime.now()
            cu.put()
            
            # replace with jenga template later probably
            self.response.out.write("<html><body>")
            self.response.out.write("<p>User added to queue, user: (%s)</p>" % (numusers+1))
            self.response.out.write("</body></html>")
            
        else:
            # replace with jenga template later probably
            self.response.out.write("<html><body>")
            self.response.out.write("<p>Too many queued users, please retry laters</p>")
            self.response.out.write("</body></html>")
        
        
        
        
app = webapp2.WSGIApplication([
    ('/requestClawAccess', RequestClawAccess),
], debug=True)