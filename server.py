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

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        self.transport.write(data)
        print data

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()

##########################################

if __name__ == '__main__':
    sysUtils.setFlags()
    
    reactor.listenTCP(PORT, EchoFactory())
    reactor.run()