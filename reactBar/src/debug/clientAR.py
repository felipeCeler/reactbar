# Cliente 
import socket
 
print "Clinte"
 
HOST='localhost' #coloca o host do servidor 
PORT=57000
 
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 
print "conectando com servidor..."
s.connect((HOST,PORT))
 
print "abrindo arquivo..."
arq=open('particle.png','rb')
 
print "enviado  arquivo"
for i in arq.readlines():
    #print i
    s.send(i)
 
print "saindo..."
arq.close()
s.close()