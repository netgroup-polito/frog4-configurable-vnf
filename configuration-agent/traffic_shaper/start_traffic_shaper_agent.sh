#!/bin/bash

if [ "$#" -lt 2 ] ; then
    echo "Error to start: usage start.sh <vnf_type> <datadisk_path> [on_change_interval(ms)]" ;
    exit;
fi

sed -i 's/10mbit/1000mbit/' /sbin/wondershaper

nf_type=$1;
datadisk_path=$2;
on_change_interval=$3;

sudo python3 -m traffic_shaper.traffic_shaper_agent $nf_type $datadisk_path $on_change_interval