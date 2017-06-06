FROM generic-image
MAINTAINER Politecnico di Torino

RUN apt-get update && apt-get install -y \ 
    iptables \
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
ADD ./nat-agent/nat nat
ADD ./nat-agent/common common
ADD ./nat-agent/start.sh start.sh
RUN chmod +x start.sh

WORKDIR /


