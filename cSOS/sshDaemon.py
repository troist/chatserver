#! /usr/bin/env python

import spur
import socket
import sys
import select
import threading
from communication import send, receive
from subprocess import Popen, PIPE, STDOUT

BUFSIZ = 1024

serverLookup = {}
clientObj = 0

def setClientObj(newClientObj):
    global clientObj
    clientObj = newClientObj

def setServerLookup(newServerLookup):
    global serverLookup
    serverLookup = newServerLookup

def initSshConnection(serverLookup, sshId, sshPort, sshUser, sshIp):
    shell = spur.SshShell(hostname=sshIp, username=sshUser, private_key_file="/home/alexj/.ssh/id_rsa", port=sshPort)
    serverLookup[sshId] = shell
    return serverLookup

def doStuff(splitList, serverLookup):

    if len(splitList) >= 4:

        if splitList[1] == 'command':

            serverObj = serverLookup.get(splitList[2])
            newList = []
            for i in splitList[3:]:
                temp = i.replace('%20', ' ')
                temp = temp.replace("'\\'", "'")
                newList.append(temp)

            print newList

            response = serverObj.run(newList).output
            singleLine = response.replace('\n', '|')

            if singleLine[-1:] == '|':
                singleLine = singleLine[:-1]

            if singleLine[:1] != '|':
                singleLine = '|' + singleLine

            singleLine = 'sshProcessor|' + splitList[2] + singleLine

            print 'Trying to return to ' + splitList[2]
            send(clientObj.sock, singleLine.strip())
        

class ChatClient(object):
    """ A simple command line chat client using select """

    def __init__(self, name, host='127.0.0.1', port=5153):

        self.name = name
        # Quit flag
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

    def cmdloop(self):

        while not self.flag:

            try:

                sys.stdout.flush()
                inputready, outputready,exceptrdy = select.select([0, self.sock], [],[])
                
                for i in inputready:

                    if i == 0:

                        continue

                    elif i == self.sock:

                        data = receive(self.sock)
                        cleanData = data.replace('\n', '')

                        if not data:

                            print 'SshDaemon Shutting down.'
                            self.flag = True
                            break

                        if cleanData.find('>> ') != -1:

                            if cleanData.split('>> ')[1] == 'Shutdown sshDaemon':

                                print 'SshDaemon Shutting down.'
                                self.flag = True
                                break

                        if cleanData[:1] == '#':

                            if cleanData.find('>> ') != -1:

                                newData = cleanData.split('>> ')[1]
                                splitData = newData.split(' ')
                                if splitData[0] == 'sshDaemon':

                                    if splitData[1] == 'shutdown':

                                        print 'SshDaemon Shutting down.'
                                        self.flag = True
                                        break

                                    if splitData[1] == 'command':

                                        doThread = threading.Thread(target = doStuff, args = (splitData, serverLookup, ))
                                        doThread.start()

                                    if splitData[1] == 'ping':

                                        if len(splitData) == 2:

                                            send(clientObj.sock, 'ok')

                                        if len(splitData) > 2:

                                            send(clientObj.sock, 'ok ' + splitData[2])

                            sys.stdout.flush()
                            
            except KeyboardInterrupt:

                print 'Interrupted.'
                self.sock.close()
                break
            
            
if __name__ == "__main__":
    #setServerLookup(initSshConnection(serverLookup, 'Porky', 2992, 'admin', '95.128.218.36'))
    #setServerLookup(initSshConnection(serverLookup, 'Twiki', 2992, 'admin', '95.128.218.37'))
    #setServerLookup(initSshConnection(serverLookup, 'Max', 2992, 'admin', '95.128.218.38'))
    #setServerLookup(initSshConnection(serverLookup, 'Kryton', 2992, 'admin', '95.128.218.39'))

    #setServerLookup(initSshConnection(serverLookup, 'QA1', 2992, 'admin', '95.128.218.47'))
    #setServerLookup(initSshConnection(serverLookup, 'QA2', 2992, 'admin', '95.128.218.48'))
    #setServerLookup(initSshConnection(serverLookup, 'QA4', 2992, 'admin', '95.128.218.45'))

    #setServerLookup(initSshConnection(serverLookup, 'Q9MaS1', 2992, 'mkadmin', '10.112.4.20'))
    #setServerLookup(initSshConnection(serverLookup, 'Q9MaS2', 2992, 'mkadmin', '10.112.4.30'))

    #setServerLookup(initSshConnection(serverLookup, 'Ash', 2992, 'admin', '95.128.219.176'))
    #setServerLookup(initSshConnection(serverLookup, 'Ember', 2992, 'admin', '95.128.219.164'))

    setServerLookup(initSshConnection(serverLookup, 'Alex', 22, 'alexj', '127.0.0.1'))
    setServerLookup(initSshConnection(serverLookup, 'Blex', 22, 'alexj', '127.0.0.1'))
    setServerLookup(initSshConnection(serverLookup, 'Clex', 22, 'alexj', '127.0.0.1'))
    setServerLookup(initSshConnection(serverLookup, 'Dlex', 22, 'alexj', '127.0.0.1'))

    client = ChatClient('sshDaemon', '127.0.0.1', 5153)
    setClientObj(client)
    client.cmdloop()
