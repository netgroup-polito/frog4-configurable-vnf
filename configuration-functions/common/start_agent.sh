#!/bin/bash

if [ "$#" -lt 2 ] ; then
    echo "Error to start: usage start.sh <vnf_type> <datadisk_path>" ;
    exit;
fi

nf_type=$1;
datadisk_path=$2;

sudo python3 start_gunicorn.py $nf_type $datadisk_path
