#!/bin/bash

if [ "$#" -lt 1 ] ; then
    echo "Error to start: usage build_dhcp-firewall_Image.sh <image_name>" ;
    exit;
fi

image_name=$1
src_dir="../../../configuration-functions"
dst_dir="dhcp-firewall-agent"

mkdir -p $dst_dir

# Copy agent's file
cp -r $src_dir/common/* $dst_dir/
cp -r $src_dir/dhcp-firewall/yang_model $dst_dir/
cp -r $src_dir/dhcp-firewall/nfs.py $dst_dir/rest_api/resources/
cp -r $src_dir/dhcp-firewall/nfs_controller.py $dst_dir/cf_core/
cp -r $src_dir/start.sh $dst_dir/

sudo docker build -t $image_name .

sudo rm -r $dst_dir

