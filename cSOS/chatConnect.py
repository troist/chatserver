#! /usr/bin/env python

import socket
import sys
import select
from communication import send, receive

BUFSIZ = 1024

class ChatClient(object):
    """ A simple command line chat client using select """

    def __init__(self, name, host='127.0.0.1', port=5153):
        self.name = name

        self.flag = False
        self.port = int(port)
        self.host = host

        try:

            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, self.port))
            send(self.sock,'NAME: ' + self.name) 
            data = receive(self.sock)
            addr = data.split('CLIENT: ')[1]

        except socket.error, e:

            print 'Could not connect to chat server @%d' % self.port
            sys.exit(1)

    def cmdloop(self, message):

        sentMessage = False
        gotResponse = False

        if  not sentMessage:
            send(self.sock, message)
            sentMessage = True

        while not self.flag and not gotResponse:

            try:

                sys.stdout.flush()
                inputready, outputready,exceptrdy = select.select([0, self.sock], [],[])
                
                for i in inputready:

                    if i == 0:

                        data = sys.stdin.readline().strip()
                        if data: send(self.sock, data)

                    elif i == self.sock:

                        data = receive(self.sock)
                        cleanData = data.replace('\n', '')

                        if not data:

                            print 'Shutting down.'
                            self.flag = True
                            break

                        if cleanData[:1] == '#':

                            newData = cleanData.split('>> ')
                            if newData[1][:12] == 'sshProcessor':

                                relevantData = newData[1].split('|')
                                splitMessage = message.split(' ')

                                if relevantData[1] == splitMessage[2]:

                                    gotResponse = True
                                    break

                            if message == 'sshDaemon ping':

                                if newData[0] == '#[sshDaemon]' and newData[1] == 'ok':

                                    gotResponse = True
                                    self.sock.close()
                                    break

            except KeyboardInterrupt:

                print 'Interrupted.'
                self.sock.close()
                break

        return newData[1]
            

def getClientObj(commandToRun):
    splitString = commandToRun.split(' ')
    client = ChatClient('sshProcessor' + splitString[2], '127.0.0.1', 5153)
    return client.cmdloop(commandToRun)
            
if __name__ == "__main__":

    client = ChatClient('sshProcessor', '127.0.0.1', 5153)
    client.cmdloop()
