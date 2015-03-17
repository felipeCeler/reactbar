"""     simpleOSC 0.2
    ixi software - July, 2006
    www.ixi-software.net

    simple API  for the Open SoundControl for Python (by Daniel Holth, Clinton
    McChesney --> pyKit.tar.gz file at http://wiretap.stetson.edu)
    Documentation at http://wiretap.stetson.edu/docs/pyKit/

    The main aim of this implementation is to provide with a simple way to deal
    with the OSC implementation that makes life easier to those who don't have
    understanding of sockets or programming. This would not be on your screen without the help
    of Daniel Holth.

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

    Thanks for the support to Buchsenhausen, Innsbruck, Austria.
"""


import osc
import socket

class Client(object):
    def __init__(self):
        self.client = {}
        self.photo = {}
    def getPhoto(self,ip,port):
        print "Servidor"
         
        HOST = str(ip)
        PORT = int(port)
         
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "Escutando a porta..."
        s.bind((HOST,PORT))
        s.listen(1)
         
        print "Aceitando a conexao..."
        conn,addr= s.accept()
         
        print "recebendo o arquivo..."
        photo = 'foto'+str(port)+'.png'
        print photo
        arq = open(photo,'wb')
        
        self.photo[port] = photo
          
        while 1:
         
             dados=conn.recv(1024)
             if not dados:
                  break
             arq.write(dados)
         
        print "saindo..."
        arq.close()
        conn.close()            
        
    def sendPhoto(self,ip,port):
    
        output = open('data.react', 'wb')
        
        # Pickle dictionary using protocol 0.
        pickle.dump(self.client, output)
        
        # Pickle the list using the highest protocol available.
        
        output.close()        
        
        host = str(msg[0][2])
        print host
        port = int(msg[0][3])+500
        print port 
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
         
        print "conectando com servidor..."
        s.connect((host,port))
         
        print "abrindo arquivo..."
        photo = 'data.react'    
        arq=open('photo','rb')
         
        print "enviado  arquivo"
        for i in arq.readlines():
            s.send(i)
         
        print "saindo..."
        arq.close()
        s.close()
# just importing the osc module creates under the hood an outbound socket and the callback manager
# (osc addressManager). But we dont have to worry about that.

c = Client()

def myTest():
    """ a simple function that creates the necesary sockets and enters an enless
        loop sending and receiving OSC
    """
    osc.init()
    
##    osc.createListener() # this defaults to port 9001 as well
    osc.listen('127.0.0.1', 40001)

    # bind addresses to functions -> printStuff() function will be triggered everytime a
    # "/test" labeled message arrives
    osc.bind(update, "/tuio/Get")
    
    import time # in this example we will have a small delay in the while loop

    print ' ready to receive and send osc messages ... FROM SERVER',40001
    
    while 1:
        #osc.sendMsg("/test", [], "127.0.0.1", 4001) # send normal msg to a specific ip and port

        time.sleep(0.5) # you don't need this, but otherwise we're sending as fast as possible.
        

    osc.dontListen() # finally close the connection bfore exiting or program


""" Below some functions dealing with OSC messages RECEIVED to Python.

    Here you can set all the responders you need to deal with the incoming
    OSC messages. You need them to the callBackManager instance in the main
    loop and associate them to the desired OSC addreses like this for example
    addressManager.add(printStuff, "/print")
    it would associate the /print tagged messages with the printStuff() function
    defined in this module. You can have several callback functions in a separated module if you wish
"""

def update(*msg):
    global c
    """deals with "print" tagged OSC addresses """
    print "printing in the printStuff function ", msg
    print "the oscaddress is ", msg[0][0]
    
    print "the value is ", msg[0][2]
    print "the value is ", msg[0][3]
    print "the value is ", msg[0][4]
    print "the value is ", msg[0][5]
    
    c.client[msg[0][3]] = []
    
    for i in range(2,len(msg[0])):
        c.client[msg[0][3]].append(msg[0][i])
            
    c.getPhoto(msg[0][2],msg[0][3])    
    
    
    
    print c.client        
                   
if __name__ == '__main__': myTest()