#!/bin/sh

# check for `sudo`
if [ $(whoami) == "root" ];
then
    sudo_cmd=""
else
    sudo_cmd="sudo"
fi

# build default
echo "Building default docker image..."
${sudo_cmd} docker build default_docker --tag ancypwn:16.04

# build 17.10
${sudo_cmd} docker build 1710_docker --tag ancypwn:17.10
