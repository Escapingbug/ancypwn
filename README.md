# ancypwn

Ancypwn is a small project to make pwn environment easily managed.

It uses docker as a seperate environment for pwn development, and provided a script to manage this docker image(container).

Currently, this can only run under linux environment. So the goal of this project for now is to provide a seperate environment for linux user who
wants to do finish some CTF pwn challenges, especially who doesn't use ubuntu but other distributions which is not used widely as pwn server.

This docker image provide:
* pwndbg
* pwntools
* keystone assmebler
* capstone disassembler
* glibc source and debug version glibc(so we can debug libc with source)
* Ropper
* ROPGadgets
* one_gadget

Nothing else for now, and it is sufficient most of the time. If you have some suggestion of what is needed or how to make this image smaller, 
it is welcome to comment an issue.

# Warning

Currently we are going through a transition phase from in-docker-terminal `lxterminal` to terminal outside. That means currently this support will be gradually added, but not instantely. If you get into any trouble, you can always fall back to pypi version instead of directly use github version. (Yes I'm just tired of managing branches) Pypi version should be working fine for now.

# Notice

Due to some miserable reason, `Python2` support is now officially dropped in this project, outside of docker. Please use `Python3` to install `ancypwn`. `notiterm` script can still be used by `Python2`.

# Installation

## Linux & MacOS Normal Setup

1. Install docker, we recommend you to let your distribution to do so.

2. we have provided you with a `Dockerfile`, you can build an image yourself. And, please do that by using given `build.sh`, run `build.sh`. If you want more customization, please refer to customization section, and understand what's under the hood.

3. Alternatively, you can pull down anciety/ancypwn:16.04, and tag it to `ancypwn:16.04`, ubuntu version number is switchable. (So anciety/ancypwn:18.10 shuld be tagged as `ancypwn:18.10`)

3. Run `python setup.py install`, or maybe you need `sudo`. Pip version is also provided and recommended `pip install ancypwn`

4. Everything should be good by now. If you got permission problems, try `sudo`, or you are using `MacOS`, see following for help.

5. If you see some error message complaining about "pull access denied" or something like that, check if your tag is corret.

## To use `pwntools` `gdb.attach` function

### MacOS

Due to bad network status, I haven't rebuild and push new docker images for now.

You can copy `notiterm/notiterm.py` to `ancypwn` accessible directory, then set this in `pwntools`:

```python
context.terminal = ['python', '/path/to/notiterm.py', '-p', '15111', '-t', 'OSXTerminal', '-e']
```

After this `gdb.attach` will give you a newly created terminal.

### Linux

Linux support for outside terminal is still being written and tested. Currently old method is used under linux.

Set your `pwntools` like this:

```python
context.terminal = ['lxterminal', '-e']
```

Note that this will give you an ugly and config-not-savable `lxterminal` only.

# Usage

```
usage: ancypwn [-h] {run,attach,end} ...

Anciety's pwn environment

positional arguments:
  {run,attach,end}  Actions you can take
    run             run a pwn thread
    attach          attach to running thread
    end             end a running thread

optional arguments:
  -h, --help        show this help message and exit

```

# Examples

During CTF games, we usually need a dynamic analysis environment to do all the dynamic stuff, but
some challenges may contain extra stuff that may taint your current linux machine.

So, we just use the `ancypwn`, and do something like this:

```
# Suppose we have a directory to save all pwnable challenges
# And we run like this

cd pwn
sudo ancypwn run .

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

# Customization

I understand that each hacker needs his own environment, and this is just my settings. Sometimes you just want to use my idea and do your own settings, and this is how you can do this.

## Under the hood

The idea is that you have a docker image containing hacking tools you need to run, and run it when you want to hack on something. The `ancypwn` program is a python script to call docker for you. What it does is just call docker with gui support, and setup a background bash to hold the docker container. Whenever you want to attach to it, it `exec`s a bash for you, so it works like a background virtual machine.

And for finding the correct image to start, it searches for tags with form `ancypwn:{ubuntu version}`, for example, if you use `ancypwn run . --ubuntu 16.04`, this will start image of name `ancypwn:16.04`.

After start the image, it will run a bash as a background process in the container to hold up the container, and whenever you want shell access, it will exec bash inside the container. This is done by saving started container name in `/tmp/ancypwn.id`.

To support outside terminal, which means to support a terminal runs outside of docker, but works like it is inside, we have a client-server structure. A client called `notiterm.py` is used, and a server
is run each time you use `ancypwn run`, and the process will be alive until you use `ancypwn end`.

Whenever you use `notiterm.py` to call for a new command run in terminal, this command will be transfered to outside server, and the server will setup a new terminal outside to run `ancypwn attach` and run the command.

## To Customize

For this reason, if you want to have your own image running with `ancypwn` script, you just need to build your own docker image, and then tag it using name `ancypwn:{ubuntu version number}`.

Actually, the ubuntu version can be anything, it just fires a warning when it is not officially ones. So you can tag a thing like `ancypwn:hello`, and use it like `ancypwn run . --ubuntu hello`.

I will consider add a more specific argument so this "ubuntu" arguments don't seem to be too strange.

# Status

Current supported version:

* 18.10
* 18.04
* 16.04

14.04 is having many issues not yet resolved.. Please fire an issue if you know how to install all the tools on 14.04, I will be appreciate.
