#!/bin/bash

if [ "$#" -lt 1 ] ; then
    echo "Error to start: usage buildIperfImage.sh <image_name>" ;
    exit;
fi

image_name=$1


sudo docker build -t $image_name .


