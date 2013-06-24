import webapp2
import logging
import os
import config.globals as gl
from model.ClawUser import ClawUser
import hashlib
import time
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# from google.appengine.api.backends.backends import get_url, get_backend, get_hostname
# from google.appengine.api.urlfetch import fetch

class RequestClawAccess(webapp2.RequestHandler):
    
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    
    def get(self):
                        
        allUsers = ClawUser().all()
        numusers = allUsers.count() #max 1000, not an issue in our case
        
        if numusers < gl.MAX_CONNECTIONS:
            
            hasher = hashlib.sha1()
            hasher.update(str(time.time()))
            channelid = hasher.hexdigest()[:20]
            timestamp = datetime.now()
        
            cu = ClawUser()
            cu.channel = channelid
            cu.timestamp = timestamp
            cu.put() # may need TransactionFailedError handling later
            
            j2_env = Environment(loader=FileSystemLoader('template'),
                         trim_blocks=True)
            
            templateVars = { 
                            "title" :           "Claw Controller Client",
                            "channel" :         channelid,
                            "timestamp" :       timestamp,
                            "sub" :             gl.SUBSCRIBE_KEY_PUBLIC,
                            "pub" :             gl.PUBLISH_KEY_PUBLIC,
                            "ssl" :             'false',
                            "queuepos" :             numusers
               }
            
            self.response.out.write( j2_env.get_template('in_queue2.html').render(templateVars) )
            
        else:
            # replace with jenga template later probably
            self.response.out.write("<html><body>")
            self.response.out.write("<p>Too many queued users, please retry laters</p>")
            self.response.out.write("</body></html>")
        
        
        
        
app = webapp2.WSGIApplication([
    ('/requestClawAccess', RequestClawAccess),
], debug=True)