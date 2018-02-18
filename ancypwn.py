#!/bin/python
import argparse
import os
import docker

EXIST_FLAG = '/tmp/ancypwn.id'

client = docker.from_env()
container = client.containers
image = client.images


class ColorWrite(object):
    COLOR_SET = {
            'END': '\033[0m',
            'yellow': '\033[38;5;226m',
            'red': '\033[31m',
            'blue': '\033[34m',
            'magenta': '\033[35m',
            'cyan': '\033[36m',
    }

    def color_write(content, color):
        print(ColorWrite.COLOR_SET[color] + content + ColorWrite.COLOR_SET['END'])


def colorwrite_init():
    for color in ColorWrite.COLOR_SET:
        # Use default value for lambda to avoid lazy capture of closure
        setattr(ColorWrite, color, lambda x, color=color: ColorWrite.color_write(x, color))

# Static initialize ColorWrite
colorwrite_init()

def parse_args():
    """Parses commandline arguments
    Returns:
        args -- argparse namespace, contains the parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Anciety's pwn environment"
    )
    subparsers = parser.add_subparsers(
        help='Actions you can take'
    )

    run_parser = subparsers.add_parser(
        'run',
        help='run a pwn thread'
    )
    run_parser.add_argument(
        'directory',
        type=str,
        help='The directory which contains your pwn challenge'
    )
    run_parser.add_argument(
        '--ubuntu',
        type=str,
        help='The version of ubuntu to open'
    )
    run_parser.set_defaults(func=run_pwn)

    attach_parser = subparsers.add_parser(
        'attach',
        help='attach to running thread',
    )
    attach_parser.set_defaults(func=attach_pwn)

    end_parser = subparsers.add_parser(
        'end',
        help='end a running thread'
    )
    end_parser.set_defaults(func=end_pwn)


    args = parser.parse_args()
    if vars(args) != {}:
        args.func(args)
    else:
        parser.print_usage()


def _read_container_name():
    if not os.path.exists(EXIST_FLAG):
        raise Exception('Pwn thread is not running')

    container_name = ''
    with open(EXIST_FLAG, 'r') as flag:
        container_name = flag.read()

    if container_name == '':
        os.remove(EXIST_FLAG)
        raise Exception('Meta info corrupted, or unable to read saved info. ' + \
                'Cleaning corrupted meta-info, please shutdown container manually')

    return container_name

def _attach_interactive(name):
    cmd = "docker exec -it {} '/bin/bash'".format(
        name
    )

    ColorWrite.yellow(
        '''
 ________      ________       ________       ___    ___  ________    ___       __       ________      
|\   __  \    |\   ___  \    |\   ____\     |\  \  /  /||\   __  \  |\  \     |\  \    |\   ___  \    
\ \  \|\  \   \ \  \\\\ \  \   \ \  \___|     \ \  \/  / /\ \  \|\  \ \ \  \    \ \  \   \ \  \\\\ \  \   
 \ \   __  \   \ \  \\\\ \  \   \ \  \         \ \    / /  \ \   ____\ \ \  \  __\ \  \   \ \  \\\\ \  \  
  \ \  \ \  \   \ \  \\\\ \  \   \ \  \____     \/  /  /    \ \  \___|  \ \  \|\__\_\  \   \ \  \\\\ \  \ 
   \ \__\ \__\   \ \__\\\ \__\   \ \_______\ __/  / /       \ \__\      \ \____________\   \ \__\\\\ \__\\
    \|__|\|__|    \|__| \|__|    \|_______||\___/ /         \|__|       \|____________|    \|__| \|__|
                                           \|___|/                                                    
        '''
    )
    os.system(cmd)



def run_pwn(args):
    """Runs a pwn thread
    Just sets needed docker arguments and run it
    """
    if not args.ubuntu:
        ubuntu = ''
    else:
        ubuntu = ':' + args.ubuntu
    if not args.directory.startswith('~') and \
            not args.directory.startswith('/'):
                # relative path
        args.directory = os.path.abspath(args.directory)

    if not os.path.exists(args.directory):
        raise FileNotFoundError('No such directory')

    if os.path.exists(EXIST_FLAG):
        raise Exception('Another pwn thread is already running')
    
    # First we need a running thread in the background, to hold existence
    running_container = container.run(
        'ancypwn{}'.format(ubuntu),
        '/bin/bash',
        cap_add=['SYS_ADMIN', 'SYS_PTRACE'],
        detach=True,
        tty=True,
        volumes={
            os.path.expanduser(args.directory) : {
                'bind': '/pwn',
                'mode': 'rw'
            }
        },
        #net='host'
    )

    # Set flag, save the container id
    with open(EXIST_FLAG, 'w') as flag:
        flag.write(running_container.name)


    # Then attach to it, needs to do it in shell since we need
    # shell to do the input and output part(interactive part)
    _attach_interactive(running_container.name)
    

def attach_pwn(args):
    """Attaches to a pwn thread
    Just sets needed docker arguments and run it as well
    """
    container_name = _read_container_name()

    # FIXME Is it better that we just exec it with given name?
    conts = container.list(filters={'name':container_name})
    assert len(conts) == 1
    _attach_interactive(conts[0].name)
    

def end_pwn(args):
    """Ends a running thread
    """
    container_name = _read_container_name()
    conts = container.list(filters={'name':container_name})
    if len(conts) < 1:
        os.remove(EXIST_FLAG)
        raise Exception('No pwn thread running, corrupted meta info file, deleted')
    conts[0].stop()
    os.remove(EXIST_FLAG)


def main():
    parse_args()


if __name__ == "__main__":
    main()
