#! /usr/bin/env python
##########################################
# 2013-07-30
# test
##########################################
# alex.jones@mkodo.com
##########################################

import chatConnect as chat

##########################################

def runTest(commandToRun):
    response = chat.getClientObj(commandToRun)
    print response

##########################################

if __name__ == '__main__':
    runTest('sshDaemon command Q9MaS1 ls')
