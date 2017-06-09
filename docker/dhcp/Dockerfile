FROM generic-image
MAINTAINER Politecnico di Torino

RUN apt-get update && apt-get install -y \
    isc-dhcp-server

#########################################################################
#									#
#			Script boot					#
#									#
#########################################################################

# Copy the agent into the docker
RUN mkdir -p /configuration_agent
WORKDIR configuration_agent
ADD ./dhcp-agent/dhcp dhcp
ADD ./dhcp-agent/common common
ADD ./dhcp-agent/start_agent.sh start_agent.sh
RUN chmod +x start_agent.sh

WORKDIR /
ADD ./dhcp-agent/start.sh start.sh
RUN chmod +x start.sh
