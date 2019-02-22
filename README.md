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

# Installation

## Linux & MacOS Normal Setup

1. Install docker, we recommend you to let your distribution to do so.

2. we have provided you with a `Dockerfile`, you can build an image yourself. And, please do that by using given `build.sh`, run `build.sh`. If you want more customization, please refer to customization section, and understand what's under the hood.

3. Alternatively, you can pull down anciety/ancypwn:16.04, and tag it to `ancypwn:16.04`, ubuntu version number is switchable. (So anciety/ancypwn:18.10 shuld be tagged as `ancypwn:18.10`)

3. Run `python setup.py install`, or maybe you need `sudo`. Pip version is also provided and recommended `pip install ancypwn`

4. Everything should be good by now. If you got permission problems, try `sudo`, or you are using `MacOS`, see following for help.

5. If you see some error message complaining about "pull access denied" or something like that, check if your tag is corret.

## MacOS GUI setup

For correctly use GUI programs (particularly, lxterminal, so that you will can use `gdb.attach()` within `pwntools`), MacOS needs to do the following(Linux users using xserver don't need to worry about these):

1. Install xquartz , you can use `brew cask install xquartz` if you are using homebrew.
2. open -a XQuartz and set it like this:
   ![](https://blog-1252049492.cos.ap-hongkong.myqcloud.com/img/Xquartz.png)
3. Now everything should be done.

### Common Problems

#### "ancypwn cannot automatically set DISPLAY"

1. First, use `ip addr show` or `ifconfig` to see what's your ip address of your using network card
2. Next, set `ANCYPWN_DISPLAY` environment variable to "[ip]:0", after these, it should be fine. You can use ancypwn and see if `lxterminal` is working.

#### "no protocol specified", lxterminal will not run

1. run "xhost +" in your xquartz terminal(bash)

#### "cannot open display IP:0"

1. check that your xquartz is running, we recommand you set it to be opened on login


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
# Term 1:
cd pwn
sudo ancypwn run .
# Now we are in a docker shell, and do something, like playing with the original binary
# Then we create another terminal, to use gdb to attach it
# The mounted directory are in `/pwn`
cd /pwn
./example_binary

# Term 2:
sudo ancypwn attach
# Now we are in the docker shell which is in the same docker machine of the previous one, but
# we have a different shell, we can use gdb to attach to the processes now
gdb
(gdb) attach PID

# We can also run exploit python script directly, you'd like to write something like `raw_input`
# to pause the process a little bit and let terminal 2 to use gdb to attach to it.
# Term 1:
python exp.py

# Term 2:
gdb
(gdb) attach PID
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

## To Customize

For this reason, if you want to have your own image running with `ancypwn` script, you just need to build your own docker image, and then tag it using name `ancypwn:{ubuntu version number}`.

Actually, the ubuntu version can be anything, it just fires a warning when it is not officially ones. So you can tag a thing like `ancypwn:hello`, and use it like `ancypwn run . --ubuntu hello`.

I will consider add a more specific argument so this "ubuntu" arguments don't seem to strange.

# Status

Current supported version:

* 18.10
* 18.04
* 16.04

14.04 is having many issues not yet resolved.. Please fire an issue if you know how to install all the tools on 14.04, I will be appreciate.
