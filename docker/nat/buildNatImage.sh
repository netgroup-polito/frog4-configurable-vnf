#!/bin/bash

if [ "$#" -lt 1 ] ; then
    echo "Error to start: usage buildNatImage.sh <image_name>" ;
    exit;
fi

image_name=$1
src_dir="../../configuration-agent"
dst_dir="nat-agent"

mkdir -p $dst_dir

# Copy the nat agent
cp -r $src_dir/common $dst_dir/
cp -r $src_dir/nat $dst_dir/
cp -r $src_dir/start_nat_agent.sh $dst_dir/start_agent.sh
cp -r $src_dir/start.sh $dst_dir/start.sh

# Extract dependencies
tar -zxvf dependencies/pynetfilter_conntrack-0.7.tar.gz -C dependencies/
tar -zxvf dependencies/python-ipy-master.tar.gz -C dependencies/

sudo docker build -t $image_name .

sudo rm -r $dst_dir
sudo rm -r dependencies/pynetfilter_conntrack-0.7
sudo rm -r dependencies/python-ipy-master