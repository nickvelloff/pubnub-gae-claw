'''
Created on Jun 13, 2013

@author: nick.velloff
'''

from backends.PubnubChannelFactory import PubnubChannelFactory
from google.appengine.api import runtime
import time
import logging
import webapp2
from google.appengine.ext import db
from model.ClawUser import ClawUser
import config.globals


class RuntimeBackendInit(webapp2.RequestHandler):
    
    # Key 1 - secure channel between claw and app
    PUBLISH_KEY_CLAW_APP_SECURE =       'pub-c-904b6a5c-c9be-4a95-ba3a-cff409a070ad'
    SUBSCRIBE_KEY_CLAW_APP_SECURE =     'sub-c-0b405dba-ce3f-11e2-9936-02ee2ddab7fe'
    SECRET_KEY_CLAW_APP_SECURE =        'sec-c-MDg0NmE0ZmMtNmE2ZC00NTFmLWI0MmQtMjE4NDkyNmM2NGZi'
    
    #Key 2 (public UNIQUE_CHANNELs for clients to get in the queue)
    PUBLISH_KEY_PUBLIC =                'pub-c-193b98ef-12c1-4657-9332-8884802c4c7d '
    SUBSCRIBE_KEY_PUBLIC =              'sub-c-aa5aac0c-d3c6-11e2-84c1-02ee2ddab7fe  '
    SECRET_KEY_PUBLIC =                 'sec-c-ZDE5YzczNzQtNGUyNy00NmQzLTkzYjMtZDljODZkOTFjYmJl'
              
    allUsersList = {}
    
    def get(self):
             
        self.__getConnectedUsers()
        self.__setupSecureChannel()

        # set shutdown hook
        runtime.set_shutdown_hook(self.isShuttingDown)

    def __setupSecureChannel(self):
        self.secureChannel = PubnubChannelFactory(
                                         self.PUBLISH_KEY_CLAW_APP_SECURE, 
                                         self.SUBSCRIBE_KEY_CLAW_APP_SECURE, 
                                         self.SECRET_KEY_CLAW_APP_SECURE, 
                                         True, 
                                         'ClawComm', 
                                         self.secureCommCallback
                                         )
        
    def __getConnectedUsers(self):
        # Get existing claw users
        # Query
        self.allUsers = ClawUser().all()
        self.allUsers.order("-timestamp")            
        results = self.allUsers.fetch(limit=config.globals.max_connections)
        for user in results:
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

