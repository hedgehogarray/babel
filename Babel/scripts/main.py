"""
Translator app.
"""

import sys
import signal

import qi

from libs import qiscript
from libs.mstranslator import Translator
from libs.mstranslator import TranslateApiException


class App(object):
    "A sample standalone app, that demonstrates simple Python usage"
    def __init__(self):
        self.qiapplication = qi.Application()
        self.qiapplication.start()
        self.session = self.qiapplication.session

        # services
        self.memory = qiscript.MemoryHelper(self.session)
        self.services = qiscript.ServiceCache(self.session)
        signal.signal(signal.SIGTERM, self.exit)

        self.phrase = None
        self.language = None
        self.translated = None

        self.languages = {'English': 'en',
                          'French': 'fr',
                          'Spanish': 'es',
                          'German': 'de',
                          'Japanese': 'ja'}

        self.translator = Translator(
            'robot-translator',
            'KEy_HERE')
        translation = self.translator.translate('hello', 'fr')
        print translation

    def exit(self):
        self.memory.clear()
        self.qiapplication.stop()

    #
    # Run functions
    #
    def ask_translation(self):
        "Ask to be touched, waits, and exits."
        self.services.ALTextToSpeech.say("Give me something to translate")
        self.memory.connect("Babel/Phrase", self.set_phrase)
        self.memory.connect("Babel/Language", self.set_language)
        self.memory.connect("Babel/Exit", self.on_exit)
        self.qiapplication.run()

    def set_phrase(self, value):
        self.phrase = value
        print self.phrase
        if self.language is not None:
            self.say_translation()

    def set_language(self, value):
        self.language = self.languages[value.title()]
        print self.language
        if self.phrase is not None:
            self.say_translation()

    def on_exit(self, value):
        if value:
            self.exit()

    def say_translation(self):
        try:
            translation = self.translator.translate(self.phrase, self.language)
            print translation
        except TranslateApiException as err:
            translation = "I'm not sure"
            print err
        self.services.ALTextToSpeech.say(translation)
        self.phrase = None
        self.language = None


def run(qi_url=None):
    # (you can also directly call this function from the python shell)
    if qi_url:
        # This will make QiApplication() connect to that robot
        sys.argv.extend(["--qi-url", qi_url])

    app = App()
    print "Successfully running on robot."
    app.ask_translation()

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

