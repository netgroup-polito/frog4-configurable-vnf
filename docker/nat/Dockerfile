FROM generic-image
MAINTAINER Politecnico di Torino

RUN apt-get update && apt-get install -y \ 
    iptables \
    bridge-utils

RUN pip3 install --upgrade pip
RUN pip3 install python-iptables

# Copy and install agent's dependencies
RUN mkdir -p /dependencies

WORKDIR dependencies
ADD ./dependencies/python-ipy-master python-ipy-master
WORKDIR python-ipy-master
RUN python3 setup.py install

WORKDIR /dependencies
ADD ./dependencies/pynetfilter_conntrack-0.7 pynetfilter_conntrack-0.7
WORKDIR pynetfilter_conntrack-0.7
RUN python3 setup.py install


#########################################################################
#									#
#			Script boot					#
#									#
#########################################################################

# Copy the agent into the docker
WORKDIR /
RUN mkdir -p /configuration_agent
WORKDIR configuration_agent
ADD ./nat-agent/nat nat
ADD ./nat-agent/common common
ADD ./nat-agent/start_agent.sh start_agent.sh
RUN chmod +x start_agent.sh

WORKDIR /
ADD ./nat-agent/start.sh start.sh
RUN chmod +x start.sh


