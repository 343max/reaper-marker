
from simpleOSC import *
import irclib
import re
import pprint
import gntp.notifier
import os.path
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("config.cfg")

oscPort = config.getint("osc", "port")
oscPath = config.get("osc", "path")
initOSCClient(port=oscPort)

# sendOSCMsg('/bot/newchapter')

#Growl
try: 
	growl = gntp.notifier.GrowlNotifier(
	    applicationName = "Crowd Marker",
	    notifications = ["New Chapter Mark"],
	    defaultNotifications = ["New Chapter Mark"]
	)
	growl.register()
except socket.error: 
	print "Growl is not running..."

# Connection information
network = config.get("irc", "network")
port    = config.getint("irc", "port") 
channel = config.get("irc", "channel") 
nick    = config.get("irc", "nick") 
name    = config.get("irc", "name")

# Create an IRC object
irc = irclib.IRC()

# Create a server object, connect and join the channel
server = irc.server()
server.connect ( network, port, nick, ircname = name )
server.join ( channel )

print "Ready to mark!"

# irclib.DEBUG = True

def newMarker(markerName):
	# setting marker
	markerFile = open('/tmp/nextMarker.txt', 'w')
	markerFile.write(markerName)
	markerFile.close()

	sendOSCMsg(oscPath)

	# grwol notification
	if growl in globals():
		growl.notify(
			noteType = "New Chapter Mark",
	 		title = "New Chapter",
	    	description = markerName
		)

	# nicecast title
	nicecastFile = open(os.path.expanduser('~/Library/Application Support/Nicecast/NowPlaying.txt'), 'w')	
	#nicecastFile = open(os.path.expanduser('NowPlaying.txt'), 'w')	
	text = "title: {0}".format(markerName)
	nicecastFile.write(text)
	nicecastFile.close()

newMarker('test!')

def handlePubMessage ( connection, event ):
	matches = re.compile('^#marker (.*)').findall(event.arguments() [ 0 ])
	if (matches != []):
		newMarker(matches[0])
		print event.target() + '> ' + event.source().split ( '!' ) [ 0 ] + ': ' + event.arguments() [ 0 ]

irc.add_global_handler ( 'pubmsg', handlePubMessage )

# Jump into an infinite loop
irc.process_forever()

