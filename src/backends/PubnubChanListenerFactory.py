'''
Created on Jun 13, 2013

@author: nick.velloff
'''

from Pubnub import Pubnub
from google.appengine.api import background_thread
import logging

class PubnubChanListenerFactory():
    
    logging.info('PubnubChannelFactory()')

    def __init__(self, 
                 publish_key, 
                 subscribe_key, 
                 secret_key = False, 
                 ssl_on = False,
                 channelName = '',
                 callbackMethod = False
                 ):
        
        self.__publish_key       = publish_key
        self.__subscribe_key     = subscribe_key
        self.__secret_key        = secret_key
        self.__ssl_on            = ssl_on
        self.__channelName       = channelName
        self.__callbackMethod    = callbackMethod if callbackMethod else self.__undefinedCallbackListener
        
        self.__initThreadedListener()
        
        
        '''
        #**
        #* PubnubChannelFactory
        #*
        #* Init PubnubChannelFactory
        #*
        #* @param string publish_key required key to send messages.
        #* @param string subscribe_key required key to receive messages.
        #* @param string secret_key required key to sign messages.
        #* @param boolean ssl_on required for 2048 bit encrypted messages.
        #* @param string origin PUBNUB Server Origin.
        #**

        ## Initiat Class
        pubnubConn = PubnubChannelFactory( 'PUBLISH-KEY', 'SUBSCRIBE-KEY', 'SECRET-KEY', Bool, 'CHANNEL-NAME', callbackMethod )

        '''
    
    def __undefinedCallbackListener(self, message):
        logging.warn('message received, but NO CALLBACK DEFINED',  message)
    
    
    def __initThreadedListener(self):
        logging.info('__initThreadedListener')
        
        # call BLOCKING subscribe method in a separate thread
        args = {'channel': self.__channelName, 
                'callback': self.__receiveComm,
                'publish_key': self.__publish_key,
                'subscribe_key': self.__subscribe_key,
                'secret_key': self.__secret_key,
                'ssl_on': self.__ssl_on
                }
        # Channel listening is BLOCKING so we are instantiating in another thread
        self.t = background_thread.BackgroundThread(target=self.__doSubscribe, kwargs=args)
        self.t.daemon = True
        self.t.start()
        
        # Type 2
#         self.tid = background_thread.start_new_background_thread(target=self.__doSubscribe, kwargs=args)
        
    def __doSubscribe(self, **kwargs):
        self.pubnubConnecor = Pubnub(kwargs['publish_key'], 
                                     kwargs['subscribe_key'], 
                                     kwargs['secret_key'], 
                                     kwargs['ssl_on']
                                     )
        
        if len( kwargs['channel'] ) > 0:
            logging.info('subscribing to channel ({})'.format(kwargs['channel']))
        
            self.pubnubConnecor.subscribe({
                'channel'  : kwargs['channel'],
                'callback' : kwargs['callback']
                })
            
        else:
            logging.info('no channel defined, listening will not begin until one is assigned via switchChannel')
            return False
    
    def switchChannel(self, newChannel):
        self.__channelName = newChannel;
        # kill thread, init new channel
     
    def __receiveComm(self, message):
        self.__callbackMethod(message)
        return True
    
    '''
    The pending BLOCKING request in the pubnub subscribe method
    can keep the thread alive when GAE is trying to shut it down
    so we just reset the callback so the message is not received twice
    '''
    def destroy(self):
        print('destroy', self, 'setting callback to ignored internal method')
        self.__callbackMethod = self.__undefinedCallbackListener
        
        
        