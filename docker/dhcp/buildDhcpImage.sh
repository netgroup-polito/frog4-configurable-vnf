#!/bin/bash

if [ "$#" -lt 1 ] ; then
    echo "Error to start: usage buildDhcpImage.sh <image_name>" ;
    exit;
fi

image_name=$1
src_dir="../../configuration-agent"
dst_dir="dhcp-agent"

mkdir -p $dst_dir

# Copy the dhcp agent
cp -r $src_dir/common $dst_dir/
cp -r $src_dir/dhcp $dst_dir/
cp -r $src_dir/start_dhcp_agent.sh $dst_dir/start_agent.sh
cp -r $src_dir/start.sh $dst_dir/start.sh

sudo docker build -t $image_name .

sudo rm -r $dst_dir
