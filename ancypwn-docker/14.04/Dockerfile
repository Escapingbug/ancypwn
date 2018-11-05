FROM ubuntu:14.04

MAINTAINER Anciety <anciety512@gmail.com>

# Apt packages (without libc source code)
RUN dpkg --add-architecture i386 && \
    sed 's/# deb-src/deb-src/g' /etc/apt/sources.list > /tmp/source && \
    mv /tmp/source /etc/apt/sources.list && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -qy \
    git nasm  python \
    build-essential \
    python-dev python-pip python-setuptools \
    xz-utils \
    libc6-dbg \
    libc6-dbg:i386 \
    gcc-multilib \
    gdb-multiarch \
    gcc \
    wget \
    curl \
    cmake \
    socat \
    netcat \
    ruby \
    libffi-dev \
    openssl \
    libssl-dev \
    lxterminal && \
    cd ~/ && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# python/ruby packages & gdb-plugin
RUN pip install --upgrade pip setuptools && pip install pwntools ropper ancypatch capstone && \
    gem install one_gadget && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# git installaing package
RUN cd ~/ && \
    git clone https://github.com/pwndbg/pwndbg.git && \
    cd ~/pwndbg/ && ./setup.sh && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV LANG C.UTF-8

VOLUME ["/pwn"]
WORKDIR /pwn

CMD ["/bin/bash"]
