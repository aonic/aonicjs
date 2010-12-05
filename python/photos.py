#!/usr/bin/env python

# Copyright (c) Raja Kapur.
# See LICENSE for details.

"""
Photos Server to push out new uploads to all connected clients using the Push Communication framework. 

Added on Nov 23, 2007: Chat functionality

Created by Raja Kapur for Photos.cx on November 2007.
"""

from twisted.internet import kqreactor
kqreactor.install()

from twisted.internet import protocol, reactor, address
from twisted.protocols.basic import LineReceiver
from twisted.spread import pb

# generate command to send to javascript interface
def getCommand(cmd, data):
    return ":%s:-%s" % (cmd, data)

# read command sent from javascript interface
def readCommand(data):
    data = data.split(':-', 1)
    return [data[0][1:], data[1].replace(':', '%3A').replace('<', '&lt;').replace('>', '&gt;')]

recentHistory = {'photo': [], 'chat': []}
    
# record recent data
def recordHistory(index, cmd, history=8):
    recentHistory[index].append(cmd)
    if len(recentHistory[index]) > history:
        recentHistory[index].pop(0)

# return recent data
def getHistory(index):
    return recentHistory[index]


class NewPhoto(pb.Root):
    
    def __init__(self, server):
        self.server = server

    def remote_newPhoto(self, password, link, thumb, number):
        # send new link to all connected users
        if(password == "secret"):
            piece = link.split('/')
            cmd = getCommand('photo', "{'link':'%s', 'thumb':'%s', 'number':'%s', 'filename':'%s'}" % (link, thumb, number, piece[3]))
            # save photo in recent photos list
            recordHistory('photo', cmd, 8)
            for session in self.server.clients:
                session.sendLine(cmd)


class NewPhotosServer(LineReceiver):
    
    username = ''
    delimiter = '\0'

    def connectionMade(self):
        self.factory.clients.append(self)

    def lineReceived(self, line):
        # send flash policy xml
        if line == "<policy-file-request/>":
            self.sendLine('<?xml version="1.0"?><cross-domain-policy><allow-access-from domain="*" to-ports="1620" /></cross-domain-policy>') 
            
        # no need for the client to be trying to talk to the server
        elif (len(line) > 350):
            log = open('/usr/local/scripts/error_log', 'a')
            log.write('Invalid Write Attempt: [%s] %d characters \r\n' % (self.transport.getPeer().host, len(line)))
            log.close()
            self.transport.loseConnection()
            
        else:
            data = readCommand(line)
            
            if(data[0] == 'username'):
                # if the user just signed on, send them the recent chat messages and photo uploads
                if self.username == '':
                    history = getHistory('photo') + getHistory('chat')
                    for cmd in history:
                        self.sendLine(cmd)
                
                self.username = data[1]
                self.sendLine(getCommand('username', self.username))
                
            elif(data[0] == 'chat'):
                cmd = getCommand('chat', "{'user':'%s', 'message':'%s'}" % (self.username, data[1]))
                # save message in recent messages list
                recordHistory('chat', cmd, 20)
                for session in self.factory.clients:
                    if self != session:
                        session.sendLine(cmd)


if __name__ == "__main__":
    
    factory = protocol.ServerFactory()
    factory.protocol = NewPhotosServer
    factory.clients = []
    
    # communication with photo_sender.py
    reactor.listenTCP(1640, pb.PBServerFactory(NewPhoto(factory)))
    # front-end users
    reactor.listenTCP(1620, factory)
    reactor.run()