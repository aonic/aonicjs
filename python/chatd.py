#!/usr/bin/env python

# Copyright (c) Raja Kapur.
# See LICENSE for details.

"""
Sample chat server to demonstrate the Push Communication framework. 
Coded in Python using the Twisted framework.

Created by Raja Kapur on November 2007.
"""

#from twisted.internet import kqreactor
#kqreactor.install()

from twisted.internet import protocol, reactor
from twisted.protocols.basic import LineReceiver

class ChatServer(LineReceiver):
    
    username = ''
    delimiter = '\0'

    def lineReceived(self, line):
        print line
        
        if line == "<policy-file-request/>":
            print "\t Sending policy file"
            self.sendLine('<?xml version="1.0"?><cross-domain-policy><allow-access-from domain="*" to-ports="3002" /></cross-domain-policy>') 
            
        elif len(line) > 350:
            file = open('./py_error_log', 'a')
            file.write('Invalid Write Attempt: [%s] %d characters \r\n' % (self.transport.getPeer().host, len(line)))
            file.close()
            self.transport.loseConnection() 
            
        elif self.username == '':
           self.factory.clients.append(self)
           self.sendLine("Welcome %s!" % line)
           self.username = line
           
        else:
            for session in self.factory.clients:
                if self != session:
                    session.sendLine("%s> %s" % (self.username, line))


if __name__ == "__main__":
    
    factory = protocol.ServerFactory()
    factory.protocol = ChatServer
    factory.clients = []
    reactor.listenTCP(3002, factory)
    reactor.run()