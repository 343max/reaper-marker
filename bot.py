
from simpleOSC import *
import irclib
import re
import pprint
import gntp.notifier
import os.path

initOSCClient(port=8000)

# sendOSCMsg('/bot/newchapter')

#Growl
growl = gntp.notifier.GrowlNotifier(
    applicationName = "Crowd Marker",
    notifications = ["New Chapter Mark"],
    defaultNotifications = ["New Chapter Mark"]
)
growl.register()

# Connection information
network = 'irc.freenode.net'
port = 6667
channel = '#reapermarkertest'
nick = 'chapterbot'
name = 'Chapter Bot'

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

	sendOSCMsg('/bot/newchapter')

	# grwol notification
	growl.notify(
		noteType = "New Chapter Mark",
 		title = "New Chapter",
    	description = markerName
	)

	# nicecast title
	nicecastFile = open(os.path.expanduser('~/Library/Application Support/Nicecast/NowPlaying.txt'), 'w')
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

