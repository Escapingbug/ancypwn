import json
import os
import multiprocessing
import struct
import importlib
from socketserver import TCPServer, StreamRequestHandler


def plugin_module_import(name):
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as e:
        prompt = 'plugin {} not found, please install it first.\n'.format(name)
        prompt += 'try follwing:\n\tpip3 install {}'.format(name)
        raise PluginNotFoundError(prompt)


class NotificationHandler(StreamRequestHandler):
    def handle(self):
        length = struct.unpack('<I', self.request.recv(4))[0]
        json_content = self.request.recv(length)
        content = json.loads(json_content)
        terminal = content['terminal']
        if content['exec'] != '':
            command = 'ancypwn attach -c \'{}\''.format(content['exec'])
        else:
            command = 'ancywn attach'
        realname = 'ancypwn_terminal_{}'.format(terminal)
        mod = plugin_module_import(realname)
        mod.run(command)


class ServerProcess(multiprocessing.Process):

    def __init__(self, port, *args, **kwargs):
        super(ServerProcess, self).__init__(*args, **kwargs)
        self.port = port

    def run(self):
        self.server = TCPServer(('', self.port), NotificationHandler)
        self.server.serve_forever()
