'''
Created on Jun 18, 2013

@author: nick.velloff
'''
from google.appengine.api import background_thread
import threading

class SubscribeThread(background_thread.BackgroundThread):
    '''
    worker thread for subscribe BLOCKING
    to enable the thread to die when needed,
    then to "unsubscrobe"
    '''


    def __init__(self):
        super(SubscribeThread, self).__init__()
        self.stoprequest = threading.Event()
        
    def run(self, **kwargs):
        
        while not self.stoprequest.isSet():
            