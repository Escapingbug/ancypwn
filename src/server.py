import json
import os
import multiprocessing
import struct
import importlib
from socketserver import TCPServer, StreamRequestHandler

class PluginNotFoundError(Exception):
    pass

def plugin_module_import(name):
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as e:
        prompt = 'plugin {} not found, please install it first.\n'.format(name)
        prompt += 'try follwing:\n\tpip3 install {}'.format(name)
        raise PluginNotFoundError(prompt)


class NotificationHandler(StreamRequestHandler):
    def handle(self):
        length = struct.unpack('<I', self.request.recv(4))[0] #第一个字节是长度
        json_content = self.request.recv(length) #接受该长度的数据
        content = json.loads(json_content) #转变json漏洞
        terminal = content['terminal']  # 选择终端
        if content['exec'] != '': # 获得执行的命令
            command = 'ancypwn attach -c \'{}\''.format(content['exec'])
        else:
            command = 'ancypwn attach'
        realname = 'ancypwn_terminal_{}'.format(terminal)
        mod = plugin_module_import(realname) #加载相关的终端模块
        mod.run(command) # 终端执行命令


class ServerProcess(multiprocessing.Process):

    def __init__(self, port, *args, **kwargs):
        super(ServerProcess, self).__init__(*args, **kwargs)
        self.port = port

    def run(self):
        self.server = TCPServer(('', self.port), NotificationHandler)
        self.server.serve_forever()
