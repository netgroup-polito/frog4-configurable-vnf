FROM      generic-configuration-agent
MAINTAINER Politecnico di Torino

RUN apt-get update && apt-get install -y iptables
ADD sysctl.conf /etc/sysctl.conf

RUN pip3 install netifaces python-iptables jsonschema
#########################################################################
#									#
#			Script boot					#
#									#
#########################################################################
WORKDIR /configuration_agent
RUN mkdir nat_config
ADD nat_config nat_config
RUN chmod +x nat_config
RUN chmod +x nat_config

#Insert template into the datadisk
WORKDIR /datadisk
ADD template.json template.json

WORKDIR /
ADD ./start_nat.sh start_nat.sh
RUN chmod +x start_nat.sh
ADD ./start_nat_agent.sh start_nat_agent.sh
RUN chmod +x start_nat_agent.sh
ADD start.sh start.sh
RUN chmod +x start.sh
