from setuptools import setup, find_packages

install_requires = [
    'docker',
    'daemonize',
]

import sys
if sys.platform == 'darwin':
    install_requires.append('osascript') # apple script support

setup(
    name='ancypwn',
    version='0.3.0.1',
    description='Ancypwn docker image manipulation script, to simplify docker pwn environment management',
    url='https://github.com/Escapingbug/ancypwn',
    author='Anciety',
    author_email='anciety512@gmail.com',
    packages=['ancypwn', 'ancypwn.notify'],
    package_dir={'ancypwn': 'src'},
    entry_points={
        'console_scripts': ['ancypwn=ancypwn.ancypwn:main']
    },
    install_requires=install_requires,
)
