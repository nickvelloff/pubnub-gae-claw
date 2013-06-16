'''
Created on Jun 13, 2013

@author: nick.velloff
'''

from backends.PubnubChannelFactory import PubnubChannelFactory
from google.appengine.api import runtime
import time
import logging
import webapp2


class PubnubBackendInit(webapp2.RequestHandler):
    
    claw_app_secure_keys_publish_key = 'pub-c-904b6a5c-c9be-4a95-ba3a-cff409a070ad'
    claw_app_secure_subscribe_key = 'sub-c-0b405dba-ce3f-11e2-9936-02ee2ddab7fe'
    claw_app_secure_keys_secret_key = 'sec-c-MDg0NmE0ZmMtNmE2ZC00NTFmLWI0MmQtMjE4NDkyNmM2NGZi'
    
    def get(self):        
        self.__setupSecureChannel()
        # set shutdown hook
        runtime.set_shutdown_hook(self.isShuttingDown)
#         self.testBlocking()

    def __setupSecureChannel(self):
        self.secureChannel = PubnubChannelFactory(
                                         self.claw_app_secure_keys_publish_key, 
                                         self.claw_app_secure_subscribe_key, 
                                         self.claw_app_secure_keys_secret_key, 
                                         True, 
                                         'ClawComm', 
                                         self.secureCommCallback
                                         )
        
    def isShuttingDown(self):
        logging.info('shutdown hook called, trying to kill BackgroundThread---------')
        self.secureChannel.destroy()
        return True
    
    def secureCommCallback(self, message):
        print(message['text'])
#         print(self)
        return True
    
    def testBlocking(self):
        while True:
            print(self, 'instance still alive')
            time.sleep(2)

app = webapp2.WSGIApplication([
    (r'/_ah/start', PubnubBackendInit),
], debug=True)

