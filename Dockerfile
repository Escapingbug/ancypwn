FROM ubuntu:xenial

MAINTAINER Anciety <ding641880047@126.com>

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -qy \
    git nasm build-essential python \
    python-dev python-pip python-setuptools \
    binutils-aarch64-linux-gnu binutils-arm-none-eabi \
    libffi-dev libssl-dev \
    libc6-dbg \
    gdb \
    gcc \
    wget \
    glibc-source libc-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# pip, pwntools, ropper
RUN pip install -U pip && \
    pip install pwntools && \
    pip install ropper

    
# Install gef

RUN wget -O ~/.gdbinit-gef.py -q https://github.com/hugsy/gef/raw/master/gef.py && \
    echo source ~/.gdbinit-gef.py >> ~/.gdbinit

# Set the locale, so that we can use unicode and send signal in gef
ENV LANG C.UTF-8

# Extract glibc source to ~
RUN cd ~/ && tar -xvf /usr/src/glibc/glibc-2.23.tar.xz

VOLUME ["/pwn"]
WORKDIR /pwn

# I personally prefer to use root user, I think that's fine for this.

CMD ["/bin/bash"]
