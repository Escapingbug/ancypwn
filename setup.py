from setuptools import setup, find_packages

setup(
    name='ancypwn',
    version='0.3.0',
    description='Ancypwn docker image manipulation script, to simplify docker pwn environment management',
    url='https://github.com/Escapingbug/ancypwn',
    author='Anciety',
    author_email='anciety512@gmail.com',
    packages=['ancypwn', 'ancypwn.notify', 'ancypwn.notify.terminal'],
    package_dir={'ancypwn': 'src'},
    entry_points={
        'console_scripts': ['ancypwn=ancypwn.ancypwn:main']
    },
    install_requires=[
        'docker',
        'appscript', # for macos Terminal interaction
    ]
)
