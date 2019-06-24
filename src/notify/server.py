"""
Notification server runs outside of docker.

The protocol used:

    [ 4 bytes length field (little endian)] + [json plain text]

Json format used:
    {
        "terminal": "iterm2",
        "exec": "command",
        "terminal_exec_command": "...", // (optional) linux user need this, 
                                        // so we know how to start a new terminal
                                        // and run command within
    }
"""
from socketserver import TCPServer, StreamRequestHandler
from .terminal import Terminal
import multiprocessing
import json
import struct
import threading
import importlib


def unpack_length(bytes_content):
    return struct.unpack('<I', bytes_content)[0]


class NotificationHandler(StreamRequestHandler):
    def handle(self):
        length = unpack_length(self.request.recv(4))
        json_content = self.request.recv(length)
        content = json.loads(json_content)

        terminal = content['terminal']
        terminal_exec_command = content.get('terminal_exec_command')
        command = '''ancypwn attach
{}'''.format(content['exec'])
        terminal_app = Terminal(terminal_exec_command).execute(terminal, command)


class NotificationServer(object):

    def __init__(self, port):
        self.port = port
        self.server = None

    def start(self):
        self.server = ForkingTCPServer(('', self.port), NotificationHandler)
        self.server.serve_forever()


class ServerProcess(multiprocessing.Process):

    def __init__(self, port, *args, **kwargs):
        super(ServerProcess,self).__init__(*args, **kwargs)
        self.port = port

    def run(self):
        self.server = TCPServer(('', self.port), NotificationHandler)
        self.server.serve_forever()
