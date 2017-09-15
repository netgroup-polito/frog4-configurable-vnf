#!/bin/bash

/usr/sbin/dhclient eth0 -v

ifconfig eth1 0
ifconfig eth2 0
brctl addbr br0
brctl addif br0 eth1
brctl addif br0 eth2
route del default
ifconfig br0 up

mkdir /etc/snort
mkdir /etc/snort/preproc_rules
mkdir /etc/snort/rules
mkdir /var/log/snort
mkdir /usr/local/lib/snort_dynamicrules
touch /etc/snort/rules/white_list.rules
touch /etc/snort/rules/black_list.rules
touch /etc/snort/rules/local.rules

chmod -R 5775 /etc/snort/
chmod -R 5775 /var/log/snort/
chmod -R 5775 /usr/local/lib/snort
chmod -R 5775 /usr/local/lib/snort_dynamicrules/

cd snort-2.9.9.0/etc && cp -avr *.conf *.map *.dtd /etc/snort/
cd .. && cp -avr src/dynamic-preprocessors/build/usr/local/lib/snort_dynamicpreprocessor/*  /usr/local/lib/snort_dynamicpreprocessor/
cd ..

sed -i "s/include \$RULE\_PATH/#include \$RULE\_PATH/" /etc/snort/snort.conf

mv /etc/snort/snort.conf /etc/snort/snort_BKP.conf