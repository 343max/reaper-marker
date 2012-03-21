from simpleOSC import *
import ConfigParser, os

config = ConfigParser.ConfigParser()
config.read("config.cfg")

oscPort = config.getint("osc", "port")
oscPath = config.get("osc", "path")

initOSCClient(port=oscPort)

sendOSCMsg(oscPath)
