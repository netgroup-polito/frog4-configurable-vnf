#!/bin/bash

if [ "$#" -ne 2 ] ; then
    echo "Error to start: usage start.sh <vnf_type> <datadisk_path>" ;
    exit;
fi

nf_type=$1;
datadisk_path=$2;

sudo python3 agent.py $nf_type $datadisk_path