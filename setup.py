from setuptools import setup, find_packages

install_requires = [
    'click',
    'appdirs',
]

setup(
    name='ancypwn',
    version='1.0.2',
    description='Ancypwn docker image manipulation script, to simplify docker pwn environment management',
    url='https://github.com/Escapingbug/ancypwn',
    author='Anciety',
    author_email='anciety@pku.edu.cn',
    packages=['ancypwn'],
    package_dir={'ancypwn': 'src'},
    entry_points={
        'console_scripts': ['ancypwn=ancypwn.ancypwn:entry']
    },
    install_requires=install_requires,
)
