from Pubnub import Pubnub

## THIS BIT ALLOWS US TO USE "urlfetch" from GAE while running from 
## Not needed in runtime 
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import urlfetch_stub

# Create a stub map so we can build App Engine mock stubs.
apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()

# Register App Engine mock stubs.
apiproxy_stub_map.apiproxy.RegisterStub(
    'urlfetch', urlfetch_stub.URLFetchServiceStub())
## -------------------------------------------------------------




## Initiat Class
pubnub = Pubnub( 'demo', 'demo', None, False )

## Publish Example
info = pubnub.publish({
    'channel' : 'hello_world',
    'message' : {
        'some_text' : 'Hello my World'
    }
})
print(info)

