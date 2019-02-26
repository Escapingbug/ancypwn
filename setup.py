from setuptools import setup

setup(
    name='ancypwn',
    version='0.2.7',
    description='Ancypwn docker image manipulation script, to simplify docker pwn environment management',
    url='https://github.com/Escapingbug/ancypwn',
    author='Anciety',
    author_email='anciety512@gmail.com',
    py_modules=['ancypwn'],
    entry_points={
        'console_scripts': ['ancypwn=ancypwn:main']
    },
    install_requires=[
        'docker',
    ]
)
