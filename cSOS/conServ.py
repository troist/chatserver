#!/usr/bin/env python

import os
import select
import socket
import sys
import signal
import time
import threading
from communication import send, receive

BUFSIZ = 1024

UUID = 0
def getUUID():
    global UUID
    UUID += 1
    return UUID

class ChatServer(object):
    """ Simple chat server using select """
    
    def __init__(self, port=5153, backlog=5):
        self.clients = 0
        # Client map
        self.clientmap = {}
        # Output socket list
        self.outputs = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('',port))
        print 'Listening to port',port,'...'
        self.server.listen(backlog)
        # Trap keyboard interrupts
        signal.signal(signal.SIGINT, self.sighandler)
        self.inputs = [self.server,sys.stdin]
        
    def sighandler(self, signum, frame):
        # Close the server
        print 'Shutting down server...'
        # Close existing client sockets
        for o in self.outputs:
            o.close()
            
        self.server.close()

    def getname(self, client):

        # Return the printable name of the
        # client, given its socket...
        info = self.clientmap[client]
        host, name = info[0][0], info[1]
        return '@'.join((name, host))

    def broadcast(self, msg):
        for o in self.outputs:
            send(o, msg)

    def printClients(self):
        outString = str(len(self.outputs))
        for out in self.outputs:
            outString += ', ' + self.getname(out)
        print outString

    def handleClients(self, s):

        if s == self.server:
        # handle the server socket
            client, address = self.server.accept()
            print 'chatserver: got connection %d from %s' % (client.fileno(), address)
            # Read the login name
            cname = receive(client).split('NAME: ')[1]
            
            # Compute client name and send back
            self.clients += 1
            send(client, 'CLIENT: ' + str(address[0]))
            self.inputs.append(client)

            self.clientmap[client] = (address, cname)
            # Send joining information to other clients
            msg = '\n(Connected: New client (%d) from %s)' % (self.clients, self.getname(client))
            if msg.find('sshProcessor') == -1:
                for o in self.outputs:
                    send(o, msg)
            
            self.outputs.append(client)

        elif s == sys.stdin:
            # handle standard input
            pass
        else:
            # handle all other sockets
            try:
                # data = s.recv(BUFSIZ)
                data = receive(s)

                print 'handling stuff ', data

                if data[:9] == 'conServer':

                    # Isolate conServer commands
                    newData = data.split(' ')

                    if len(newData) > 1:
                        if newData[1] == 'command':

                            if len(newData) > 2:
                                if newData[2] == 'start':

                                    if len(newData) > 3:

                                        exists = False
                                        for o in self.outputs:
                                            if (self.getname(o)).find(newData[3]) != -1:
                                                exists = True

                                        if not exists:
                                            print 'Trying to start ' + newData[3]
                                            os.system('nohup ./' + newData[3] + '.py &')

                                if newData[2] == 'stop':

                                    if len(newData) > 3:
                                        print 'Trying to stop ' + newData[3]

                                        for o in self.outputs:
                                            if (self.getname(o)).find(newData[3]) != -1:
                                                send(o, '\n' + '#[conServer@127.0.0.1]>> ' + newData[3] + ' shutdown')
                                                self.clients -= 1
                                                o.close()
                                                self.inputs.remove(o)
                                                self.outputs.remove(o)

                                                msg = '\n(Hung up: Client from %s)' % self.getname(o)
                                                for z in self.outputs:
                                                    send(z, msg)

                                if newData[2] == 'clients':

                                    clientString = ''
                                    for o in self.outputs:
                                        clientString += self.getname(o) + ', '

                                    self.broadcast(clientString[:-2])

                        if newData[1] == 'shutdown':
                            running = 0

                if data:
                    name = self.getname(s).split('@')
                    msg = '\n#[' + name[0] + ']>> ' + data
                    for o in self.outputs:
                        if o != s:
                            print 'BROARDCAST fired at ', self.getname(o)
                            send(o, msg)
                        else:
                            print 'Not fired at ', self.getname(o)
                        self.printClients()
                        #time.sleep(0.1)

                else:
                    print '#### %s hung up' % self.getname(s)
                    self.clients -= 1
                    s.close()
                    inputs.remove(s)
                    self.outputs.remove(s)

                    # Send client leaving information to others
                    msg = '\n(Hung up: Client from %s)' % self.getname(s)
                    if msg.find('sshProcessor') == -1:
                        for o in self.outputs:
                            send(o, msg)
                        
            except socket.error, e:
                # Remove
                self.inputs.remove(s)
                self.outputs.remove(s)


        self.server.close()

    def serve(self):
        
        running = 1

        while running:

            try:
                inputready,outputready,exceptready = select.select(self.inputs, self.outputs, [])
            except select.error, e:
                break
            except socket.error, e:
                break

            for s in inputready:

                cThread = threading.Thread(target = self.handleClients, args = (s, ))
                cThread.start()


if __name__ == "__main__":
    ChatServer().serve()
