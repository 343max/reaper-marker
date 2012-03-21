from simpleOSC import *


initOSCClient(port=8000)

sendOSCMsg('/bot/newchapter')
