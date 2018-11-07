#!/bin/sh

# check for `sudo`
if [ $(whoami) == "root" ];
then
    sudo_cmd=""
else
    sudo_cmd="sudo"
fi

# build default
echo "Building 16.04 docker image..."
${sudo_cmd} docker build ancypwn-docker/16.04 --tag ancypwn:16.04

# build 18.10
#${sudo_cmd} docker build ancypwn-docker/18.10 --tag ancypwn:18.10

# build 14.04
#${sudo_cmd} docker build ancypwn-docker/14.04 --tag ancypwn:14.04
