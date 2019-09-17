#!/usr/bin/python

import argparse
import json
import struct
import socket


def pack(num):
    return struct.pack('<I', num)


def main():
    parser = argparse.ArgumentParser('fake terminal that connects to outside world')
    parser.add_argument('-e', required=True, help='execute command in outside terminal')
    parser.add_argument('-t', '--terminal', required=True, help='terminal execute command')
    parser.add_argument('-p', '--port', type=int, help='port used outside')
    parser.add_argument('-s', '--server', required=True, help='host server')

    args = parser.parse_args()

    cmd = args.e
    terminal = args.terminal
    port = args.port if not args.port is None else 15111
    server = args.server

    msg = {
        'exec': cmd,
        'terminal': args.terminal
    }
    msg_json = json.dumps(msg)
    length = len(msg_json)
    protocol_msg = pack(length) + msg_json

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args.server, port))

    sock.sendall(protocol_msg)
    

if __name__ == '__main__':
    main()