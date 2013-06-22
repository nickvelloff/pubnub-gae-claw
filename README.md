# Client, Server, Claw app flows

The general purpose of this app is to:

The project uses the [Pubnub Python library](https://github.com/pubnub/pubnub-api/tree/master/python/)
PubNub 3.3 Web Data Push Cloud-hosted API - PYTHON
www.pubnub.com - PubNub Web Data Push Service in the Cloud. 
http://github.com/pubnub/pubnub-api/tree/master/python

## Keys (TEMP sandbox keys)
Key 1 (secret channel for claw)  
Subscribe Key		sub-c-0b405dba-ce3f-11e2-9936-02ee2ddab7fe  
Publish Key			pub-c-904b6a5c-c9be-4a95-ba3a-cff409a070ad  
Secret Key			sec-c-MDg0NmE0ZmMtNmE2ZC00NTFmLWI0MmQtMjE4NDkyNmM2NGZi  

Key 2 (public UNIQUE_CHANNELs for clients to get in the queue)
Subscribe Key		sub-c-aa5aac0c-d3c6-11e2-84c1-02ee2ddab7fe  
Publish Key			pub-c-193b98ef-12c1-4657-9332-8884802c4c7d  
Secret Key			sec-c-ZDE5YzczNzQtNGUyNy00NmQzLTkzYjMtZDljODZkOTFjYmJl

## General Notes
	- Claw is a "dumb client", and is instructed what channel to listen to over secure connection to App (GAE)
	- Claw maintains persistent connection to secure app channel, sub/pub
	- Claw when ready to be controlled will switch and listen to temp channel that is user controlled
	- App assigns clients unique channel IDs so they can be identified individually
	- Apps general purpose is to manage client connections and queuing

## General technical client flow
	- Client request unique channel from API - UNIQUE_CHANNEL, returns queue location (0...n), shows user
	- Client registers to UNIQUE_CHANNEL channel on key set 2, subscribe, publish (two way)
	- Client waits for 0 then messages "get ready your up"
	- Client receives message when claw is listening to their UNIQUE_CHANNEL {'control':true}
	
	- Client sends controlling instructions:
		{'command':'upOn'}, {'command':'upOff'}, {'command':'rightOn'}, {'command':'rightOff'} ...
	- Client receives "end" command {'control':false} and disconnects from channel "unsubscribe"
	
## General technical server flow

	### App startup (or restart)
		- App loads any existing clients with UNIQUE_CHANNELs from db (class ClawUser)
		- App sets up pubnub instance to publish on key set 2
		- App publishes update to all clients on all UNIQUE_CHANNEL channels, noting their position in the queue "updateClients()"
		
		
		- App registers to "ClawComm" channel on key set 1, subscribe, publish (two way)
			Only App and Claw apps have pub/sub keys to channel set 1 so it is secure
		- App registers to presence on "ClawComm" channel, begins listening to connects/disconnects
		- App receives "claw status" and sets internal state
		
	### Upon "claw status" update from claw over "ClawComm"
		- Claw states:
			CLAW_READY - indicates claw is ready to receive a new user
				If available, gets oldest queued client and removes from queue list
					If client is no longer present channel is removed and move to next queued client
				Publishes to claw the UNIQUE_CHANNEL to listen to for client direct control of claw
				Publishes unique channel id to claw over "ClawComm" channel
				updateClients() - to alert them of their position in the queue
				
			CLAW_CONTROLLED - indicates client is being controlled by a client
			CLAW_OFFLINE - probably detected by presence on ClawComm channel
	
	### Upon detection of client connect/disconnect
		- App adds/removes user to in memory client list
		- updateClients()		
			
## General technical claw flow	
	
	### Claw startup
		- Claw registers to "ClawComm" channel on key set 1, subscribe, publish (two way)
		- Claw sends CLAW_READY over "ClawComm"
		- Claw listens for CHANNEL_LISTEN request over secure channel
		
	### Claw receives CHANNEL_LISTEN request containing UNIQUE_CHANNEL
		- Claw sends CLAW_CONTROLLED
		- Claw registers to UNIQUE_CHANNEL channel on key set 2, subscribe, publish (two way)
		
	### Claw completes control cycle - enters resting/complete state
		- Claw will auto disconnect from UNIQUE_CHANNEL (if connected)
		- Claw sends CLAW_READY over "ClawComm"