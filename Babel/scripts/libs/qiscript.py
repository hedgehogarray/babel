"""
qiscript.py

A helper function for making simple standalone python scripts as apps.

Wraps some NAOqi and system stuff, you could do all this by directly using the
Python SDK, these helper functions just isolate some frequently used/hairy
bits so you don't have them mixed in your logic.

Copyright Aldebaran Robotics
ekroeger@aldebaran.com
"""

__version__ = "0.0.5"

__copyright__ = "Copyright 2015, Aldebaran Robotics"
__author__ = 'ekroeger'
__email__ = 'ekroeger@aldebaran.com'

import qi
#
# Helpers for making sure we have a robot to connect to
#

def check_commandline_args(description):
    "Checks whether command-line parameters are enough"
    import argparse
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--qi-url', help='connect to specific naoqi instance')

    args = parser.parse_args()
    return bool(args.qi_url)

def get_debug_robot():
    "Returns IP address of debug robot, complaining if not found"
    try:
        import qiq.config
        qiqrobot = qiq.config.defaultHost()
        if qiqrobot:
            #print "Running on qiq's", robot
            robot = raw_input("connect to which robot? (default is {0})".format(qiqrobot))
            if robot:
                return robot
            else:
                return qiqrobot
        else:
            print "qiq found, but it has no default robot configured."
    except ImportError:
        # qiq not installed
        print "qiq not installed (you can use it to set a default robot)."
    return raw_input("connect to which robot? ")

#
# Helpers for NAOqi services
#

class MemoryHelper:
    "Helper for ALMemory; takes care of event connections so you don't have to"
    def __init__(self, session):
        self.session = session
        self.almemory = session.service("ALMemory")
        self.handlers = {} # a handler is (subscriber, connections)

    def connect(self, event, callback):
        "connects an event to a callback"
        if event not in self.handlers:
            self.handlers[event] = (self.almemory.subscriber(event), [])
        subscriber, connections = self.handlers[event]
        connection_id = subscriber.signal.connect(callback)
        connections.append(connection_id)
        return connection_id

    def disconnect(self, event, connection_id=None):
        "Disconnects a connection, or all if no connection is specified."
        if event in self.handlers:
            subscriber, connections = self.handlers[event]
            if connection_id:
                if connection_id in connections:
                    subscriber.signal.disconnect(connection_id)
                    connections.remove(connection_id)
            else:
                # Didn't specify a connection ID: remove all
                for connection_id in connections:
                    subscriber.signal.disconnect(connection_id)
                del connections[:]

    def clear(self):
        "Disconnect all connections"
        for event in list(self.handlers):
            self.disconnect(event)

    def get(self, key):
        return self.almemory.getData(key)

    def set(self, key, value):
        return self.almemory.raiseEvent(key, value)

    def _on_wait_event(self, value):
        if value == self.wait_value:
            self.wait_value = None
            self.event_promise.setValue(True)

    def wait_for(self, event, value, verbose=False):
        "Block until a certain event is raised"
        if self.get(event) == value:
            if verbose:
                print "Not listening to {0}, it's already {1}".format(event, value)
            return
        self.wait_value = value
        self.event_promise = qi.Promise()
        connection_id = self.connect(event, self._on_wait_event)
        if verbose:
            print "Listening to {0}, waiting for {1}".format(event, value)
        self.event_promise.future().value()
        if verbose:
            print "Listening to {0}, got {1} !".format(event, value)
        self.disconnect(event, connection_id)


class ServiceCache:
    "A helper for accessing NAOqi services."
    def __init__(self, session):
        self.session = session
        self.services = {}

    def __getattr__(self, servicename):
        if servicename[0] == "_":
            raise AttributeError
        if (not (servicename in self.services)) or (servicename =="ALTabletService"):
            # ugly hack: never cache ALtabletService, always ask for a new one
            try:
                self.services[servicename] = self.session.service(servicename)
            except Exception as e:
                print "Error getting %s: %s" % (servicename, str(e))
                self.services[servicename] = None
        return self.services[servicename]


