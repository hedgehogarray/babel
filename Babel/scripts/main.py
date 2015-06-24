"""
A sample showing how to make a standalone Python script as an app.

This doesn't venture into fancy multithreading yet.

Copyright Aldebaran Robotics
ekroeger@aldebaran.com
"""

__version__ = "0.0.5"

__copyright__ = "Copyright 2015, Aldebaran Robotics"
__author__ = 'ekroeger'
__email__ = 'ekroeger@aldebaran.com'

import sys
import signal

import qi

from libs import qiscript

class App(object):
    "A sample standalone app, that demonstrates simple Python usage"
    def __init__(self):
        self.qiapplication = qi.Application()
        self.qiapplication.start()
        self.session = self.qiapplication.session

        #services
        self.memory = qiscript.MemoryHelper(self.session)
        self.services = qiscript.ServiceCache(self.session)
        signal.signal(signal.SIGTERM, self.exit)

    def exit(self):
        self.memory.clear()
        self.qiapplication.stop()

    def on_touched(self, value):
        if value:
            self.memory.disconnect("FrontTactilTouched")
            print "Forehead touched!"
            self.services.ALTextToSpeech.say("Yay!")
            self.exit()

    #
    # Run functions
    #
    def run_ask_touch(self):
        "Ask to be touched, waits, and exits."
        # Two ways of waiting for events
        # 1) block until it's called
        self.services.ALTextToSpeech.say("Touch my forehead")
        self.memory.wait_for("FrontTactilTouched", 1.0)

        # 2) explicitly connect a callback
        self.memory.connect("FrontTactilTouched", self.on_touched)
        self.services.ALTextToSpeech.say("okay, touch it again")
        # note that we connect the callback before the ALTextToSpeech,
        # so touch events are received while the robot is speaking (not possible
        # with the wait_for version above).

        # now run until someone calls .exit()
        self.qiapplication.run()

    def run_simple(self):
        "Just raise an ALmemory, say 'um', and exit."
        self.memory.set("PythonApp/Test", True)
        self.services.ALTextToSpeech.say("um")
        self.exit()


def run(qi_url=None):
    # (you can also directly call this function from the python shell)
    if qi_url:
        # This will make QiApplication() connect to that robot
        sys.argv.extend(["--qi-url", qi_url])

    app = App()
    print "Successfully running on robot."
    app.run_ask_touch()
    #app.run_simple()

    print "App Finished, exiting."
    app.services.ALTextToSpeech.say("Cleaning up")
    # other cleanup goes here

####################
# Run configuration
####################

if __name__ == "__main__":
    print "=============================================="
    if qiscript.check_commandline_args('Run the app.'):
        run()
    else:
        print "no --qi-url parameter given; interactively getting debug robot."
        debug_robot = qiscript.get_debug_robot()
        if debug_robot:
            run(qi_url=debug_robot)
        else:
            print "No robot, not running."

