#!/bin/python3
import click
import importlib
import json
import os
import appdirs
import platform
import pathlib

APPNAME = 'ancypwn'
APPAUTHOR = 'Anciety'


CONFIG_DIR = appdirs.user_data_dir(APPNAME, APPAUTHOR)
CONFIG_FILE_PATH = os.path.join(CONFIG_DIR, 'config.json')


SUPPORTED_UBUNTU_VERSION = [
    '16.04',
    '18.04',
    '18.10',
]


system = platform.system().lower()
if 'linux' in system or 'darwin' in system:
    BACKEND_DEFAULT_CONFIG = {
        'name': 'unix'
    }
    if 'linux' in system:
        install_plugin_name = 'linux'
    else:
        install_plugin_name = 'darwin'
else:
    # windows
    BACKEND_DEFAULT_CONFIG = {
        'name': 'windows_remote',
        'url': 'tcp://localhost:2375',
    }
    install_plugin_name = 'windows'


DEFAULT_CONFIG = {
    'terminal_port': 15111,
    'backend': BACKEND_DEFAULT_CONFIG,
    # install plugin name
    'install_plugin': install_plugin_name,
}

config = DEFAULT_CONFIG
backend = None
install_plugin = None


class PluginNotFoundError(Exception):
    pass


def plugin_module_import(name):
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as e:
        prompt = 'plugin {} not found, please install it first.\n'.format(name)
        prompt += 'try follwing:\n\tpip3 install {}'.format(name)
        raise PluginNotFoundError(prompt)


class InstallPlugin:
    def __init__(self, config):
        name = config['install_plugin']
        realname = 'ancypwn_install_{}'.format(name)
        self.config = config
        self.mod = plugin_module_import(realname)

    def install(self):
        self.mod.install(self.config)


class Backend:
    def __init__(self, config):
        realname = 'ancypwn_backend_{}'.format(config['backend']['name'])
        self.config = config
        self.mod = plugin_module_import(realname)

    def run(self, directory=None, priv=None, image=None, tag=None, command=None):
        if directory is None or \
            priv is None or \
            image is None or \
            tag is None or \
            command is None:
            # this should never hapen
            raise Exception('backend run argument incorrect!')
        image_name = '{}:{}'.format(image, tag)
        self.mod.run(
            config=self.config,
            priv=priv,
            image_name=image_name,
            directory=directory,
            command=command,
        )

    def attach(self, command):
        self.mod.attach(self.config, command)

    def end(self):
        self.mod.end(self.config)


@click.group()
def entry():
    global config, backend

    if not os.path.exists(CONFIG_DIR):
        pathlib.Path(CONFIG_DIR).mkdir(parents=True, exist_ok=True)

    if not os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, 'w') as f:
            json.dump(DEFAULT_CONFIG, f)
    else:
        with open(CONFIG_FILE_PATH, 'r') as f:
            config = json.load(f)

    backend = Backend(config)


@click.command()
def install():
    global install_plugin
    install_plugin = InstallPlugin(config)
    install_plugin.install()


@click.command()
@click.option(
    '--directory',
    default='.',
    type=click.Path(exists=True),
    help='directory to be mounted as /pwn'
)
@click.option('--priv', default=False, help='start docker in privileged mode')
@click.option('--tag',
    default='16.04',
    help='tag of the image, ' + \
        'if using official image, this is ubuntu version, one of ' + \
        ', '.join(SUPPORTED_UBUNTU_VERSION))
@click.option('--image',
    default='ancypwn',
    help='image name, if not sure, use default')
@click.option('-c', '--command',
    default='',
    help='command to execute when run')
def run(directory, priv, tag, image, command):
    backend.run(
        directory=directory,
        priv=priv,
        image=image,
        tag=tag,
        command=command)

@click.command()
@click.option('-c', '--command', default='', help='command to execute when attach')
def attach(command):
    backend.attach(command)

@click.command()
def end():
    backend.end()

entry.add_command(run)
entry.add_command(attach)
entry.add_command(end)
entry.add_command(install)
