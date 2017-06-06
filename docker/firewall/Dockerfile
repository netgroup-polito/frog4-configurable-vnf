FROM generic-image
MAINTAINER Politecnico di Torino

RUN apt-get update && apt-get install -y \
    iptables \
    ebtables \
    bridge-utils

RUN pip3 install --upgrade pip
RUN pip3 install python-iptables

#########################################################################
#									#
#			Script boot					#
#									#
#########################################################################

# Copy the agent into the docker
RUN mkdir -p /configuration_agent
WORKDIR configuration_agent
ADD ./firewall-agent/firewall firewall
ADD ./firewall-agent/common common
ADD ./firewall-agent/start_agent.sh start_agent.sh
RUN chmod +x start_agent.sh

WORKDIR /
ADD ./nat-agent/start.sh start.sh
RUN chmod +x start.sh
