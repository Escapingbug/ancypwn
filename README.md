# ancypwn
Ancypwn is a small project to make pwn environment easily managed.

It uses docker as a seperate environment for pwn development, and provided a script to manage this docker image(container).

Currently, this can only run under linux environment. So the goal of this project for now is to provide a seperate environment for linux user who
wants to do finish some CTF pwn challenges, especially who doesn't use ubuntu but other distributions which is not used widely as pwn server.

This docker image provide:
* gef
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

**Linux :**

1. Install docker, we recommend you to let your distribution to do so.
2. Since the image is too huge to upload, we provide you a `Dockerfile`, you can build an image yourself. And, please do that by using given `build.sh`, run `build.sh` under linux distribution where `docker` is provided should be sufficient. If not? Please give me an issue and describe what's wrong.
3. Run `python setup.py install`, or maybe you need `sudo`. Pip version is also provided and recommended `pip install ancypwn`
4. Everything should be good by now. If you got permission problems, try `sudo`

**MacOS** :

1. Install docker

2. Then Install  xquartz , `brew cask install xquartz`

3. open -a XQuartz and set it like this:

   ![](https://blog-1252049492.cos.ap-hongkong.myqcloud.com/img/Xquartz.png)

4. Final , use ancypwn script and fun it !

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
