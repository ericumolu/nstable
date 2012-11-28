#!/usr/local/bin/python3.1

#    This file is part of nstable.
#
#    nstable is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    nstable is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

import re, fileinput, sys, os.path, subprocess

class nstable:

    def __init__(self):
        self.cat6 = 'cat6'
        self.table = {}
        self.listenTable = {}

        self.cat0 = ""
        self.cat1 = ""
        self.cat2 = ""
        self.cat3 = ""
        self.cat4 = ""
        self.cat5 = ""
    
        self.left =  15  
        self.center = 80

        self.longSep = '-' * (self.center + self.left)
        self.shortSep = '-' * self.center
        self.connTotal = 0 
        self.inOn = 0
        self.inOff = 0
        self.outOn = 0
        self.outOff = 0
        self.stdinOn = 0
        self.listing = []
        self.hosts = []
        self.fileOut = None
        self.fileErr = None

    def setCat0(self):
        self.table[self.cat0] = {}
    
    def setCat1(self):
        self.table[self.cat0][self.cat1] = {}

    def setCat2(self):
        self.table[self.cat0][self.cat1][self.cat2] = {}

    def setCat3(self):
        self.table[self.cat0][self.cat1][self.cat2][self.cat3] = {}

    def setCat4(self):
        self.table[self.cat0][self.cat1][self.cat2][self.cat3][self.cat4] = {}

    def setCat5(self):
        self.table[self.cat0][self.cat1][self.cat2][self.cat3][self.cat4][self.cat5] = {}

    def setCat6(self):
        self.table[self.cat0][self.cat1][self.cat2][self.cat3][self.cat4][self.cat5][self.cat6] = 0
        self.upCount()
            
    def upCount(self):
        self.table[self.cat0][self.cat1][self.cat2][self.cat3][self.cat4][self.cat5][self.cat6] += 1   
        self.connTotal += 1 

    def check(self):
        if self.cat0 not in self.table:
            self.setCat0()
            self.setCat1()
            self.setCat2()
            self.setCat3()
            self.setCat4()
            self.setCat5()
            self.setCat6()

        elif self.cat1 not in self.table[self.cat0]:
            self.setCat1()
            self.setCat2()
            self.setCat3()
            self.setCat4()
            self.setCat5()
            self.setCat6()

        elif self.cat2 not in self.table[self.cat0][self.cat1]:
            self.setCat2()
            self.setCat3()
            self.setCat4()
            self.setCat5()
            self.setCat6()

        elif self.cat3 not in self.table[self.cat0][self.cat1][self.cat2]:
            self.setCat3()
            self.setCat4()
            self.setCat5()
            self.setCat6()

        elif self.cat4 not in self.table[self.cat0][self.cat1][self.cat2][self.cat3]:
            self.setCat4()
            self.setCat5()
            self.setCat6()
    
        elif self.cat5 not in self.table[self.cat0][self.cat1][self.cat2][self.cat3][self.cat4]:
            self.setCat5()
            self.setCat6()
        else:
            self.upCount()

    def set(self,c0, c1, c2, c3, c4, c5):
        self.cat0 = c0
        self.cat1 = c1
        self.cat2 = c2
        self.cat3 = c3
        self.cat4 = c4
        self.cat5 = c5
        
        self.check()
    
    def nsout(self):
        self.setFile()
        command = subprocess.Popen(["netstat" ,"-tuan"],stdout=self.fileOut, stderr=self.fileErr)
        command.communicate()
        self.closeFile()

    def setListen(self, c0, c1):
        if c0 not in self.listenTable:
            self.listenTable[c0] = {}
        self.listenTable[c0][c1] = {}
    
    def getHosts(self):
        self.setFile()
        line = " "
        for host in self.hosts:
            command = subprocess.Popen(["ssh", "root@"+host ,"netstat" ,"-tuan"],stdout=self.fileOut, stderr=self.fileErr)
            command.communicate()
        self.closeFile()

    def getstdin(self):
        self.setFile()
        line = " "
        while line:
            line = sys.stdin.readline()
            self.fileOut.write(line)
        self.closeFile()

    def setFile(self):
        self.fileOut = open(sys.path[0] + "/ns.out",'w')
        self.fileErr = open(sys.path[0] + "/ns.err",'w')

    def closeFile(self):
        self.fileOut.close()
        self.fileErr.close()

    def nsin(self):
        local = remote = protocol = dir = state = port = portLocal = portRemote = ""    
        for lineIn in open(sys.path[0] + '/ns.out'):
            lineSplit = lineIn.split()
        
            if lineSplit[0] in 'udptcp' :
                protocol = lineSplit[0]
                local , portLocal = lineSplit[3].split(':')[-2:]
                
                if local == '':
                    local = '0.0.0.0'

                remote , portRemote = lineSplit[4].split(':')[-2:]

                if portRemote == '*':
                    self.setListen(local, portLocal)
                else:
                    if int(portLocal) <= int(portRemote):
                        dir = 'In'
                        port = portLocal
                    else:   
                        dir = 'Out' 
                        port = portRemote

                    state = lineSplit[5]

                    if state == 'ESTABLISHED':
                        state = 'On'
                    else:   
                        state = 'Off'

                    self.set(local, protocol, remote , dir, state, port)

    def show(self):
        for keycat0 in self.table:
            self.listing = []
            
            self.cat0 = keycat0
            self.line0()

            for keycat1 in self.table[keycat0]:
                self.cat1 = keycat1
                self.line1()
                self.line2()
                self.line3()
                self.line4()

                for keycat2 in self.table[keycat0][keycat1]:
                    self.cat2 = keycat2

                    for keycat3 in self.table[keycat0][keycat1][keycat2]:
                        self.cat3 = keycat3
                        
                        for keycat4 in self.table[keycat0][keycat1][keycat2][keycat3]:
                            self.cat4 = keycat4

                            for keycat5 in self.table[keycat0][keycat1][keycat2][keycat3][keycat4]:
                                self.cat5 = keycat5
                                    
                                for keycat6 in self.table[keycat0][keycat1][keycat2][keycat3][keycat4][keycat5]:
                                    self.cat6 = str(self.table[keycat0][keycat1][keycat2][keycat3][keycat4][keycat5][keycat6])

                                    self.listing.append([self.cat2, self.cat3 , self.cat4, self.cat5, self.cat6 ])
            self.sortList()
            self.middle()
            self.bottom()

    def showListen(self):
        smallCenter = int((self.center / 8 ) - 1)
        print ('\n' * 2)
        print ('LISTEN'.center(25))
        print ('-' * 25)
        print ('(local)'.ljust(self.left) + 'Port'.center(smallCenter))

        for keycat0 in self.listenTable:
            print ('-' * 25)
            print (keycat0.ljust(self.left))
            print
            for keycat1 in self.listenTable[keycat0]:
                print (''.ljust(self.left) + keycat1.center(smallCenter))


    def line0(self):
        print ('\n' * 2)
        print (''.ljust(self.left) + ('(local)'+self.cat0).center(self.center))
        print (''.ljust(self.left) + self.shortSep)

    def line1(self):
        print (''.ljust(self.left) + self.cat1.center(self.center))
        print (''.ljust(self.left) + self.shortSep)
        
    def line2(self):
        smallCenter = int((self.center / 2 ) - 1)
        print (''.ljust(self.left) + 'Inbound'.center(smallCenter) + '[]' + 'Outbound'.center(smallCenter))
        print (''.ljust(self.left) + self.shortSep)

    def line3(self):
        smallCenter = int((self.center / 4 ) - 1)
        state = 'On'.center(smallCenter) + '|' + 'Off'.center(smallCenter) 
        print (''.ljust(self.left) + state + '[]' + state)
        print (''.ljust(self.left) + self.shortSep)

    def line4(self):
        smallCenter = int((self.center / 8 ) - 1)
        port = 'Port'.center(smallCenter) + '|' + 'Count'.center(smallCenter) 
        print ('(remote)'.ljust(self.left) + port +'|'+ port +'[]'+ port+'|' + port)

    def middle(self):
        smallCenter = int((self.center / 8 ) - 1)
        for item in self.listing:
            
            box1=''.center(smallCenter) + '|' + ''.center(smallCenter)
            box2=''.center(smallCenter) + '|' + ''.center(smallCenter)
            box3=''.center(smallCenter) + '|' + ''.center(smallCenter)
            box4=''.center(smallCenter) + '|' + ''.center(smallCenter)

            self.cat2 = item[0]
            self.leftSide()

            if item[1] == 'In':
                if item[2] == 'On':
                    box1=item[3].center(smallCenter) + '|' + item[4].center(smallCenter)
                    self.inOn += int(item[4])
                else:
                    box2=item[3].center(smallCenter) + '|' + item[4].center(smallCenter)
                    self.inOff += int(item[4])
            else:
                if item[2] == 'On':
                    box3=item[3].center(smallCenter) + '|' + item[4].center(smallCenter)
                    self.outOn += int(item[4])
                else:
                    box4=item[3].center(smallCenter) + '|' + item[4].center(smallCenter)
                    self.outOff += int(item[4])

            print (''.ljust(self.left) +  box1 +'|'+ box2 +'[]'+ box3+'|' + box4)
    
    def leftSide(self):
        smallCenter = int((self.center / 8 ) - 1)
        box=''.center(smallCenter) + '|' + ''.center(smallCenter)
        print (self.longSep)
        print (self.cat2.ljust(self.left) + box +'|'+ box +'[]'+ box+'|' + box)

    def bottom(self):
        smallCenter = int((self.center / 8 ) - 1)
        box1=''.center(smallCenter) + '|' + str(self.inOn).center(smallCenter)
        box2=''.center(smallCenter) + '|' + str(self.inOff).center(smallCenter)
        box3=''.center(smallCenter) + '|' + str(self.outOn).center(smallCenter)
        box4=''.center(smallCenter) + '|' + str(self.outOff).center(smallCenter)

        all = self.inOn + self.inOff + self.outOn + self.outOff

        print (self.longSep)
        print (('Total: '+str(all)).ljust(self.left) + box1 +'|'+ box2 +'[]'+ box3+'|' + box4)
        print
    
    def sortList(self):
        rev = False
        sortBy = 'all'
        self.listing = sorted(self.listing, key=lambda item: int(item[4]), reverse = rev)

    def getArgv(self):
        index = 1
        while index < len(sys.argv):
            if sys.argv[index] == '-i':
                self.stdinOn = 1
                index += 1
            elif sys.argv[index] == '-h':
                index += 1
                while index < len(sys.argv) and sys.argv[index][0] != '-' :
                    self.hosts.append(sys.argv[index])
                    index += 1
            else:
                index += 1 

if __name__== '__main__' :

    table = nstable()
    table.getArgv()

    if table.stdinOn:
        table.getstdin()    
    elif len(table.hosts):
        table.getHosts()
    else:
        table.nsout()

    table.nsin()
    table.showListen()
    table.show()
    #print table.listenTable
