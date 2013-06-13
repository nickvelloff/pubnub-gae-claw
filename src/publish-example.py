from Pubnub import Pubnub

## Initiate Class
pubnub = Pubnub( 'demo', 'demo', None, False )

## Publish Example
info = pubnub.publish({
    'channel' : 'my_channel',
    'message' : {
        'some_text' : 'Whats up Hollywood!'
    }
})
print(info)

