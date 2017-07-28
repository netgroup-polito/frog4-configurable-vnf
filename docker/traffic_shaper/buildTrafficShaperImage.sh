#!/bin/bash

if [ "$#" -lt 1 ] ; then
    echo "Error to start: usage buildTrafficShaperImage.sh <image_name>" ;
    exit;
fi

image_name=$1
src_dir="../../configuration-agent"
dst_dir="traffic-shaper-agent"

mkdir -p $dst_dir

# Copy the dhcp agent
cp -r $src_dir/common $dst_dir/
mkdir $dst_dir/components
cp -r $src_dir/components/common $dst_dir/components/common/
cp -r $src_dir/vnf_template_library $dst_dir/
cp -r $src_dir/traffic_shaper $dst_dir/
cp -r $src_dir/traffic_shaper/start_traffic_shaper_agent.sh $dst_dir/start_agent.sh
cp -r $src_dir/start.sh $dst_dir/start.sh

sudo docker build -t $image_name .

sudo rm -r $dst_dir
