#! /usr/bin/env python
##########################################
# 2013-08-03
# makeFile
# v1.0
##########################################
# alex.jones@mkodo.com
##########################################
# Imports

from sysUtils import vPrint
import sysUtils
import datetime
import os

##########################################

hashLine = '##########################################'

def makeFile():

    stringToWrite = ''

    fileName = sysUtils.getFlagBody('f')
    if fileName[-2:] == 'py':
        stringToWrite += '#! /usr/bin/env python'

    if fileName[-2:] == 'sh':
        stringToWrite += '#! /bin/bash'

    stringToWrite += '\n' + hashLine + '\n'
    stringToWrite += '# ' + datetime.datetime.now().strftime('%Y-%m-%d') + '\n'
    stringToWrite += '# ' + fileName[:fileName.find('.')] + '\n'

    if sysUtils.getFlagBody('n') != -1:
        stringToWrite += '# v' + sysUtils.getFlagBody('n') + '\n'

    stringToWrite += hashLine + '\n# alex.jones@mkodo.com\n' + hashLine + '\n'

    # Imports
    stringToWrite += '# Imports\n\n'

    if sysUtils.checkFlag('s') != -1:
        stringToWrite += 'from sysUtils import vPrint\n'
        stringToWrite += 'import sysUtils\n'

    stringToWrite += '\n' + hashLine + '\n\n\n\n' + hashLine + '\n'


    # Main function
    stringToWrite += '\n' + "if __name__ == '__main__':\n"

    if sysUtils.checkFlag('s') != -1:
        stringToWrite += '    sysUtils.setFlags()\n'

    stringToWrite += "    print 'Hello World!'"

    vPrint(stringToWrite)

    sysUtils.writeToFile(sysUtils.getFlagBody('f'), stringToWrite)

def makeExecutable():
    if sysUtils.checkFlag('x') != -1:
        os.system('chmod 755 ' + sysUtils.getFlagBody('f'))

def copySysUtils():
    if sysUtils.checkFlag('s') != -1:
    os.system('cp ' + sysUtils.getLocation() + '/sysUtils.py .')

##########################################

if __name__ == '__main__':
    sysUtils.setFlags()
    makeFile()
    makeExecutable()
    copySysUtils()
