# ancypwn

Ancypwn is your one-key-to-all CTF pwnable challenges environment helper.

It uses docker to manage the tools you might need, so you have separete environment, and you do all the debugging with the shared folder.

(all official pips have been uploaded, enjoy.)

## Provided tools

* pwndbg
* pwntools
* keystone assmebler
* capstone disassembler
* glibc source and debug version glibc(so we can debug libc with source)
* Ropper
* ROPGadgets
* one_gadget
* seccomp-tools

## Installation

Ancypwn is now plugin based, choose your own plugin or write a new plugin if you need more flexible config/environment support.

### Overview

You will need at least 4 parts to have a working environment (apart from docker).

0. A ancypwn docker image, and is properly tagged as ancypwn:VERSION, VERSION is one of "16.04", "18.04" or "18.10", each represent a corresponding ubuntu version.
1. ancypwn launcher (`pip install ancypwn`)
2. a backend: backend provides ability to listen incoming request to pop up a terminal window, then asks terminal plugin to do it and does different docker container launching strategy (like remote support).
3. a terminal plugin: this one handles terminal poping up

Backends have the name pattern: `ancypwn-backend-*`, while terminal plugin has the pattern `ancypwn-terminal-*`.

So you need:

```
# build images
docker build -t ancypwn:20.04 .
docker build -t ancypwn:18.04 .
docker build -t ancypwn:18.10 .
docker build -t ancypwn:16.04 .

pip3 install ancypwn
# install ancypwn-backend-* (choose your backend, and install it)
# install ancypwn-terminal-* (choose your terminal, and install it)
```

### Choose your backend

Current official backends:

- [ancypwn-backend-windows_remote](https://github.com/Escapingbug/ancypwn-backend-windows_remote)
- [ancypwn-backend-macos](https://github.com/Escapingbug/ancypwn-backend-macos)

### Choose your terminal

Current official terminals:

- [ancypwn-terminal-alacritty](https://github.com/Escapingbug/ancypwn-terminal-alacritty)
- [ancypwn-terminal-iterm2](https://github.com/shizhongpwn/ancypwn-terminal-iterm2.git)

## Usage

ancypwn is just a docker launcher, and support one instance at a time.

You can do:

* `ancypwn run`: runs the docker, and mount current directory by default to `/pwn`, then you will be passed to the docker shell, do your debugging here
* `ancypwn end`: stops the docker
* `ancypwn attach`: ancypwn run may already be done, without ending, you can attach to the previously run instance, then you will be passed to the docker shell.

Internally, `ancypwn` command can be seen as just a docker commandline runner, so you don't need to remember the sophisticated docker arguments.
You can also run your own docker image, by using `ancypwn run --image YOUR_IMAGE --tag YOUR_TAG`.

## To use `pwntools` `gdb.attach` function

What the best of `ancypwn` is its supporting of popping up terminal window and runs command inside. This allows the fluent experience of using pwntools' `gdb.attach` function to debug target.

To use this, you need to set up your terminal like this:

```
context.terminal = ['ancyterm', '-s', '[HOST_ADDRESS]', '-p', '15111', '-t', '[TERMINAL]', '-e']
```

This is a little bit verbose, let me explain:

- `-s [HOST_ADDRESS]`: this is required to access host from docker, depends on exact backend. For example, `ancypwn-backend-macos` backend requires `host.docker.internal` to be the host address.
- `-p 15111`: the port of the server, 15111 by default.
- `-t [TERMINAL]`: the terminal plugin name. For example, `alacritty` for `ancypwn-terminal-alacritty`.

## Configuration

Config is handled by `appdirs`, under `author = Anciety`, `appname = ancypwn` setting. Different OS may have different directory, please refer to [appdirs](https://pypi.org/project/appdirs/) for more information.

When you launch ancypwn the first time, a default configuration will be written to `CONFIG_DIR/config.json`.

Some of the configurations are:

- `backend`: a key-value pair, required at least a "name" to note which backend to use, others are required by specific backend
- `terminal_port`: the port to run terminal popping up service, 15111 by default. 
- `install_plugin`: not available feature for now, ignore it.

## Common Problems

### Mac OSX "objc[1895]: +[NSString initialize] may have been in progress in another thread when fork() was called."

Reported by one of the users, I haven't met this situation, thus I have no idea why this is happening.

Solution is set this environment variable:

```
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```

## Examples

During CTF games, we usually need a dynamic analysis environment to do all the dynamic stuff, but
some challenges may contain extra stuff that may taint your current linux machine.

So, we just use the `ancypwn`, and do something like this:

```
# Suppose we have a directory to save all pwnable challenges
# And we run like this

cd pwn
sudo ancypwn run

# Now we are in a docker shell, and do something, like playing with the original binary
# Then we create another terminal, to use gdb to attach it
# The mounted directory are in `/pwn`
cd /pwn
./example_binary

# In another terminal, you should edit your exploit. Set the pwntools settings like above mentioned.
# Then run it like normal.
python exploit.py
# If you used gdb.attach, it should create a new terminal for you.
```

In general, this simple script only provides you a direct way of using docker. All things are done
by docker itself. The script just makes the docker act like a real "virtual machine".

Since many challenges use different `libc`s, this can also be achieved. By default, "17.10" and
"16.04" of ubuntu is provided, if you need others, commit an issue, please. And they can be used
use `--ubuntu 17.10`. `16.04` is used by default.

# Status

Current supported ubuntu version:

* 18.10
* 18.04
* 16.04
* 20.04
