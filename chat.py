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

chatServer = "localhost"
PORT = 1234

##########################################

class ClientProtocol(Protocol):

    def sendMessage(self, msg):
        self.transport.write("%s\n" % msg)

    def dataReceived(self, data):
        print data


def gotProtocol(p):
    p.sendMessage("Hello")
    reactor.callLater(1, p.sendMessage, "This is sent in a second")
    #eactor.callLater(2, p.transport.loseConnection)

##########################################

if __name__ == '__main__':
    sysUtils.setFlags()

    point = TCP4ClientEndpoint(reactor, chatServer, PORT)
    d = connectProtocol(point, ClientProtocol())
    d.addCallback(gotProtocol)
    reactor.run()