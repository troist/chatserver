#! /usr/bin/env python
##########################################
# 2013-08-03
# server
# v0.1
##########################################
# alex.jones@mkodo.com
##########################################
# Imports

from sysUtils import vPrint
import sysUtils

from twisted.internet import protocol, reactor
from twisted.internet.protocol import Protocol

##########################################

PORT = 1234

##########################################

class Echo(Protocol):

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.numProtocols = self.factory.numProtocols+1 
        self.transport.write(
            "Welcome! There are currently %d open connections.\n" %
            (self.factory.numProtocols,))

    def connectionLost(self, reason):
        self.factory.numProtocols = self.factory.numProtocols-1

    def dataReceived(self, data):
        self.transport.write(data)

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()



##########################################

if __name__ == '__main__':
    sysUtils.setFlags()
    
    reactor.listenTCP(PORT, EchoFactory())
    reactor.run()

    print 'Server listening on port ' + str(PORT)