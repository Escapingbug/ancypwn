import os
from sys import platform
import osascript

class Terminal(object):

    def __init__(self, terminal_exec_command):
        self.terminal_exec_command = terminal_exec_command

    def mac_execute(self, terminal, command):

        def iterm_exec(cmd):
            apple_script = '''tell application "iTerm2"
    tell current session of current window
        select split vertically with default profile
        write text "{}"
    end tell
end tell
'''.format(cmd)
            osascript.run(apple_script)

        def terminal_exec(cmd):
            apple_script = '''tell application "Terminal"
    do script("/bin/bash -c {}")
end tell'''.format(cmd)
            osascript.run(apple_script)

        terminal = terminal.lower()
        if terminal == 'iterm' or terminal == 'iterm2':
            iterm_exec(command)
        elif terminal == 'terminal':
            terminal_exec(command)
        else:
            raise Exception('This terminal is not yet supported on Mac OSX')


    def execute(self, terminal, command):
        if platform == 'darwin':
            self.mac_execute(terminal, command)
        else:
            raise NotImplemented('os aside from Mac OSX is not yet implemented')
