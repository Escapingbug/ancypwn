from .term import Terminal
import appscript


class OSXTerminal(object):

    def __init__(self):
        self.app = appscript.app('Terminal')

    def execute(self, command):
        self.app.do_script(command)
