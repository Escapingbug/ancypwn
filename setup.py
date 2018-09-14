from setuptools import setup

setup(
    name='ancypwn',
    version='0.2.3-1810',
    description='Ancypwn docker image manipulation script, to simplify docker pwn environment management',
    url='https://github.com/Escapingbug/ancypwn',
    author='Anciety',
    author_email='ding641880047@126.com',
    py_modules=['ancypwn'],
    entry_points={
        'console_scripts': ['ancypwn=ancypwn:main']
    },
    install_requires=[
        'docker'
    ]
)
