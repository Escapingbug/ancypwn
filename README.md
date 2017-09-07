# ancypwn
Ancypwn is a small project to make pwn environment easily managed.

It uses docker as a seperate environment for pwn development, and provided a script to manage this docker image(container).

Currently, this can only run under linux environment. So the goal of this project for now is to provide a seperate environment for linux user who
wants to do finish some CTF pwn challenges, especially who doesn't use ubuntu but other distributions which is not used widely as pwn server.

This docker image provide:
* debug version libc and its source under ubuntu
* gef
* pwntools

Nothing else for now, and it is sufficient most of the time. If you have some suggestion of what is needed or how to make this image smaller, 
it is welcome to comment an issue.

# Installation
1. Install docker, we recommend you to use your distribution to do so.
2. Since the image is too huge to upload, we provide you a `Dockerfile`, you can build an image yourself. And, please do that.
3. Run `python setup.py install`, or maybe you need `sudo`
4. Everything should be good by now. If you got permission problems, try `sudo`

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
