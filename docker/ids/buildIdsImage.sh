#!/bin/bash

if [ "$#" -lt 1 ] ; then
    echo "Error to start: usage buildIperfImage.sh <image_name>" ;
    exit;
fi

image_name=$1
src_dir="../../configuration-agent"
dst_dir="ids-agent"

mkdir -p $dst_dir

# Copy the dhcp agent
cp -r $src_dir/common $dst_dir/
mkdir $dst_dir/components
cp -r $src_dir/components/common $dst_dir/components/common/
cp -r $src_dir/components/ids $dst_dir/components/ids/
cp -r $src_dir/vnf_template_library $dst_dir/
cp -r $src_dir/ids $dst_dir/
cp -r $src_dir/ids/start_ids_agent.sh $dst_dir/start_agent.sh
cp -r $src_dir/start.sh $dst_dir/start.sh

sudo docker build -t $image_name .

sudo rm -r $dst_dir

