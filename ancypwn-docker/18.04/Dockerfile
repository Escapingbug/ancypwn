FROM ubuntu:18.04

MAINTAINER Anciety <anciety512@gmail.com>


# Apt packages
RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get -y install sudo wget cmake curl gcc socat\
    software-properties-common && \
    wget http://archive.ubuntu.com/ubuntu/pool/main/k/keyutils/libkeyutils1_1.5.9-9.2ubuntu2_amd64.deb && \
    dpkg -i libkeyutils1_1.5.9-9.2ubuntu2_amd64.deb && \
    add-apt-repository ppa:brightbox/ruby-ng && \
    apt-get update && \
    apt-get purge --auto-remove ruby && \
    DEBIAN_FRONTEND=noninteractive apt-get install -qy \
    git nasm python3 \
    build-essential \
    python3-dev python3-pip python3-setuptools \
    libc6-dbg \
    libc6-dbg:i386 \
    gcc-multilib \
    gdb-multiarch \
    glibc-source \
    netcat \
    ruby2.6 \
    ruby2.6-dev \
    lxterminal && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    cd ~ && tar -xvf /usr/src/glibc/glib*.tar.xz

# python/ruby packages & gdb-plugin
RUN wget https://bootstrap.pypa.io/pip/3.5/get-pip.py && \
    python3 get-pip.py && \
    pip install --no-cache-dir LibcSearcher pwntools ropper ancypatch && \
    gem install one_gadget seccomp-tools && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# git installaing package
RUN cd ~/ && \
    git clone https://github.com/pwndbg/pwndbg.git && \
    cd ~/pwndbg/ && ./setup.sh && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN cd ~/ && \
    git clone https://github.com/scwuaptx/Pwngdb.git && \
    cp ~/Pwngdb/.gdbinit ~/ && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    sed -i '1d' ~/.gdbinit && \
    sed -i '1c source ~/pwndbg/gdbinit.py' ~/.gdbinit*

ENV LANG C.UTF-8

COPY ./ancyterm.py /usr/local/bin/ancyterm
RUN chmod +x /usr/local/bin/ancyterm

VOLUME ["/pwn"]
WORKDIR /pwn

CMD ["/bin/bash"]
