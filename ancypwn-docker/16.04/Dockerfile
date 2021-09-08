FROM ubuntu:16.04

MAINTAINER Anciety <anciety512@gmail.com>

# Apt packages
RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get -y install python-software-properties \
    software-properties-common && \
    add-apt-repository ppa:brightbox/ruby-ng && \
    apt-get update && \
    apt-get purge --auto-remove ruby && \
    DEBIAN_FRONTEND=noninteractive apt-get install -qy \
    git nasm python3 \
    build-essential \
    python3-dev python3-pip python3-setuptools\
    libc6-dbg \
    libc6-dbg:i386 \
    gcc-multilib \
    gdb-multiarch \
    gcc \
    sudo \
    wget \
    curl \
    glibc-source \
    cmake \
    socat \
    netcat \
    ruby2.6 \
    ruby2.6-dev \
    lxterminal && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    cd ~ && tar -xvf /usr/src/glibc/glibc-2.23.tar.xz

# python/ruby packages & gdb-plugin
#RUN wget https://files.pythonhosted.org/packages/cd/82/04e9aaf603fdbaecb4323b9e723f13c92c245f6ab2902195c53987848c78/pip-21.1.2-py3-none-any.whl && \
#RUN pip3 install pip-21.1.2-py3-none-any.whl && \
RUN wget https://bootstrap.pypa.io/pip/3.5/get-pip.py && \
    python3 get-pip.py && \
#    pip3 install --upgrade pip && \
    pip3 install --no-cache-dir pwntools ropper ancypatch LibcSearcher&& \
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
    sed -i '1c source ~/pwndbg/gdbinit.py' ~/.gdbinit

ENV LANG C.UTF-8

COPY ./ancyterm.py /usr/local/bin/ancyterm
RUN chmod +x /usr/local/bin/ancyterm

VOLUME ["/pwn"]
WORKDIR /pwn

CMD ["/bin/bash"]
