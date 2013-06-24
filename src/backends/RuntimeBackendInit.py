'''
Created on Jun 13, 2013

@author: nick.velloff
'''

from backends.PubnubChanListenerFactory import PubnubChanListenerFactory
from google.appengine.api import runtime
import time
import logging
import webapp2
from google.appengine.ext import db
from model.ClawUser import ClawUser
import config.globals as gl
from Pubnub import Pubnub

class RuntimeBackendInit(webapp2.RequestHandler):
    
    # contains a list of all connected ClawUser objects      
    allUsersList = []
    
    def get(self):
             
        self.__getConnectedUsers()
        self.__setupSecureChannel()
        self.__setupClientChannel()
        
        # set shutdown hook
        runtime.set_shutdown_hook(self.isShuttingDown)

    def __setupSecureChannel(self):
        self.secureChannel = PubnubChanListenerFactory(
                                         gl.PUBLISH_KEY_CLAW_APP_SECURE, 
                                         gl.SUBSCRIBE_KEY_CLAW_APP_SECURE, 
                                         gl.SECRET_KEY_CLAW_APP_SECURE, 
                                         True, 
                                         'ClawComm', 
                                         self.secureCommCallback
                                         )
        
    def __setupClientChannel(self):
        self.publishClient = Pubnub(gl.PUBLISH_KEY_PUBLIC, gl.SUBSCRIBE_KEY_PUBLIC, gl.SECRET_KEY_PUBLIC, False)
        
    def __getConnectedUsers(self):
        # Get existing claw users
        # Query
        self.allUsers = ClawUser().all()
        self.allUsers.order("-timestamp")            
        self.allUsersList = self.allUsers.fetch(limit=gl.MAX_CONNECTIONS)
    
    
    def __updateConnectedUsers(self):
        for user in self.allUsersList:
            print user.channel
            
    
    def isShuttingDown(self):
#         logging.info('shutdown hook called, trying to kill BackgroundThread---------')
        
        self.secureChannel.destroy()
        return True
    
    def secureCommCallback(self, message):
        logging.info(message['text'])
        return True
    
    
    def testBlocking(self):
        while True:
            logging.info(self, 'instance still alive')
            time.sleep(2)



app = webapp2.WSGIApplication([
    (r'/_ah/start', RuntimeBackendInit),
#     ('/be', RuntimeBackendInit),
], debug=True)

