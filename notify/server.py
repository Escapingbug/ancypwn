"""
Notification server runs outside of docker.

The protocol used:

    [ 4 bytes length field (little endian)] + [json plain text]

Json format used:
    {
        "terminal": "OSXTerminal",
        "exec": "command"
    }
"""
from socketserver import TCPServer, StreamRequestHandler
import multiprocessing
import json
import struct
import threading
import importlib


def unpack_length(bytes_content):
    return struct.unpack('<I')[0]


class NotificationHandler(StreamRequestHandler):
    def handle(self):
        length = unpack_length(self.request.recv(4))
        json_content = self.request.recv(length)
        content = json.loads(json_content)

        terminal = content['terminal']
        term_mod = importlib.import_module('term.{}'.format(terminal))
        terminal_app = getattr(term_mod, terminal)

        command = '''
        ancypwn attach
        {}
        '''.format(content['exec'])

        terminal_app.execute(command)


class NotificationServer(object):

    def __init__(self, port):
        self.port = port
        self.server = None

    def start(self):
        self.server = ForkingTCPServer(('', self.port), NotificationHandler)
        self.server.serve_forever()


class ServerProcess(multiprocessing.Process):

    def __init__(self, daemon_pid_path, port, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.daemon_pid_path = daemon_pid_path
        self.port = port

    def run(self):
        with open(self.daemon_pid_path, 'w') as f:
            f.write(str(self.pid))
        self.server = TCPServer(('', self.port), NotificationHandler)
        self.server.serve_forever();
