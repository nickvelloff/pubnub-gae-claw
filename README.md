# Claw Google App Engine Python Application

This app is the central business and application logic layer for the claw.

The general purpose of this app is to:

* Manage client connections and queuing
* Manage claw channels and overall controller

The project uses the [Pubnub Python library](https://github.com/pubnub/pubnub-api/tree/master/python/)
PubNub 3.3 Web Data Push Cloud-hosted API - PYTHON
www.pubnub.com - PubNub Web Data Push Service in the Cloud. 
http://github.com/pubnub/pubnub-api/tree/master/python

## Keys (these are all demo sandboxed so just get your own)
Key 1 (secret channel for claw)
Subscribe Key	sub-c-0b405dba-ce3f-11e2-9936-02ee2ddab7fe
Publish Key	pub-c-904b6a5c-c9be-4a95-ba3a-cff409a070ad
Secret Key	sec-c-MDg0NmE0ZmMtNmE2ZC00NTFmLWI0MmQtMjE4NDkyNmM2NGZi

Key 2
Subscribe Key	sub-c-aa5aac0c-d3c6-11e2-84c1-02ee2ddab7fe
Publish Key	pub-c-193b98ef-12c1-4657-9332-8884802c4c7d
Secret Key	sec-c-ZDE5YzczNzQtNGUyNy00NmQzLTkzYjMtZDljODZkOTFjYmJl

### Working claw flow:
	- detect network connection, launch infinitely running python script
	- subscribe ("ClawComm" channel) to Key 1 (secret channel for claw) for direct comm b/t gae app and claw app - Publish, Subscribe (2 way comm)
	- claw client app is essentially a "dumb client", and is completely controlled by the GAE App
	- claw only offers status messages over ClawComm to GAE App
	- claw will receive message over ClawComm to
		- disconnect from current "temporary client channel" (if connected) 
		- connect to new "temporary client channel" with supplied name
		- listen for commands to control claw
		- probably auto select "insert quarter"
		- message client over "temporary client channel" to begin controlling
		- before disconnect, message client over "temporary client channel" to resign control - wont matter either way because claw will stop listening 
		
	- claw will auto disconnect from "temporary client channel" when claw rests in ending state

### GAE App flow (needs to be over SSL):
	App to claw communication
	- launch GAE "Backends" long running process (TBD)
	- subscribe ("ClawComm" channel) to Key 1 (secret channel for claw) for direct comm b/t gae app and claw app - Publish, Subscribe (2 way comm)
	- secret channel for claw uses Secret key to sign messages - use SSL on
	- ClawComm will communicate claw status
		- ready, inprocess (TBD)
	- app will assign the claw "presence id" and monitor connection status (join, leave, reconnect)
	
	App to client communication
	- subscribe ("ClientComm" channel) to Key 2 (open channel for client) for client live queuing - Publish, Subscribe (2 way comm)
		- until queuing system is in place, every new client will be granted access to claw and kick anyone else off (channel reset)
		- this channel is only used to request access to the claw, and will ultimately give clients their queue position
		- when claw is ready to receive a new client, app send message over ClawComm and assigns a new channel id
			- app maintains channel names, unique to requesting client to ensure only one client can connect to claw
			- 
		- when 
	- 

### Claw Client flow:
	- 
	- 

