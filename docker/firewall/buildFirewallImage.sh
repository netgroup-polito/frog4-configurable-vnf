#!/bin/bash

if [ "$#" -lt 1 ] ; then
    echo "Error to start: usage buildFirewallImage.sh <image_name>" ;
    exit;
fi

image_name=$1
src_dir="../../configuration-agent"
dst_dir="firewall-agent"

mkdir -p $dst_dir

# Copy the firewall agent
cp -r $src_dir/common $dst_dir/
cp -r $src_dir/firewall $dst_dir/
cp -r $src_dir/start_firewall_agent.sh $dst_dir/start.sh

sudo docker build -t $image_name .

sudo rm -r tmp
