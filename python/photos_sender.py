#!/usr/bin/env python

# Copyright (c) Raja Kapur.
# See LICENSE for details.

"""
Photos Sender client to send new photos to the Photos Server.

Created by Raja Kapur for Photos.cx on November 2007.
"""

import sys
from twisted.spread import pb
from twisted.internet import reactor
from twisted.python import usage

class Options(usage.Options):

    optParameters = [
        ["password", "p", None, "secret password"],
        ["link", "l", None, "photo link"],
        ["thumb", "t", None, "photo thumbnail link"],
        ["number", "n", 0, "photo number"],
        ["host", "h", "localhost", "server host"],
        ["port", "P", 1640, "server port"]
    ]
    
    def opt_version(self):
        print 'PCX Photo Sender 0.5'
        sys.exit(0)
    
    def paramError(self, errortext):
        print '%s: %s' % (sys.argv[0], errortext)
        print '%s: Try --help for usage details.' % (sys.argv[0])
        sys.exit(0)


if __name__ == "__main__":
    
    config = Options()
    
    try:
        config.parseOptions()
    
        if (config['password'] is not None) and (config['link'] is not None):
            factory = pb.PBClientFactory()
            root = factory.getRootObject()
            root.addCallback(lambda object: object.callRemote('newPhoto', config['password'], config['link'], config['thumb'], config['number']))
            root.addErrback(lambda _: reactor.stop())
            root.addCallback(lambda _: reactor.stop())
            
            reactor.connectTCP(config['host'], int(config['port']), factory)
            reactor.run()
        else:
            raise usage.UsageError, 'invalid password or link'
            
    except usage.UsageError, errortext:
        config.paramError(errortext)