# Claw User Flows

## General technical client flow
	- Client registers to "ClawComm" channel on key set 2, subscribe only (one way)
	- Client receives location in queue (0...n), shows user
	- Client waits for 0 then messages "get ready your up"
	- Upon 0, client receives message {'channelSwap':CHANNEL_ID, 'subKey':KEY, 'pubKey':KEY} 
	- Client disconnects from "ClawComm" channel
	- Client connects (SSL) to CHANNEL_ID channel with KEYS (key set 3)
	- Client sends controlling instructions:
		{'command':'upOn'}, {'command':'upOff'}, {'command':'rightOn'}, {'command':'rightOff'} ...
	- Client receives "end" command and disconnects from channel "unsubscribe"
	
## General technical server flow
	- App receives 