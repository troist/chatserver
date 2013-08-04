#! /usr/bin/env python
##########################################
# 2013-08-03
# chat
# v0.1
##########################################
# alex.jones@mkodo.com
##########################################
# Imports

from sysUtils import vPrint
import sysUtils

from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol

##########################################

class Greeter(Protocol):
    def sendMessage(self, msg):
        self.transport.write("MESSAGE %s\n" % msg)

def gotProtocol(p):
    p.sendMessage("Hello")
    reactor.callLater(1, p.sendMessage, "This is sent in a second")
    reactor.callLater(2, p.transport.loseConnection)

##########################################

if __name__ == '__main__':
    sysUtils.setFlags()
    point = TCP4ClientEndpoint(reactor, "localhost", 1234)
    d = connectProtocol(point, Greeter())
    d.addCallback(gotProtocol)
    reactor.run()
    print "Chat client running"
