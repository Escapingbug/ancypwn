#!/bin/python
import argparse
import json
import struct
import socket

def pack(num):
    return struct.pack('<I', num)


def main():
    parser = argparse.ArgumentParser('fake terminal that connects to outside world')
    parser.add_argument('-e', required=True, help='execute command in outside terminal')
    parser.add_argument('-t', '--terminal', required=True, help='terminal to use (if possible to choose)')
    parser.add_argument('-p', '--port', required=True, help='port used outside')

    args = parser.parse_args()

    cmd = args.e
    terminal = args.terminal

    msg = {
        'exec': cmd,
        'terminal': args.terminal
    }
    msg_json = json.dumps(msg)
    length = len(msg_json)
    protocol_msg = pack(length)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('host.docker.internal', args.port))

    sock.sendall(protocol_msg)
    

if __name__ == '__main__':
    main()
