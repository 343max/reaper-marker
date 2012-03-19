
from simpleOSC import *
import irclib

initOSCClient(port=8000)

# sendOSCMsg('/bot/newchapter')


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

# irclib.DEBUG = True

def handlePubMessage ( connection, event ):
   print event.target() + '> ' + event.source().split ( '!' ) [ 0 ] + ': ' + event.arguments() [ 0 ]

irc.add_global_handler ( 'pubmsg', handlePubMessage )

# Jump into an infinite loop
irc.process_forever()

