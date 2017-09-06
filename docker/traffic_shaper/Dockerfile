FROM generic-image
MAINTAINER Politecnico di Torino

RUN apt-get update && apt-get install -y \
    wondershaper

#########################################################################
#									#
#			Script boot					#
#									#
#########################################################################

WORKDIR /

# Copy the agent into the docker
RUN mkdir -p /configuration_agent
WORKDIR configuration_agent
ADD ./traffic-shaper-agent/traffic_shaper traffic_shaper
ADD ./traffic-shaper-agent/common common
ADD ./traffic-shaper-agent/components components
ADD ./traffic-shaper-agent/vnf_template_library vnf_template_library
ADD ./traffic-shaper-agent/start_agent.sh start_agent.sh
RUN chmod +x start_agent.sh

WORKDIR /
ADD ./traffic-shaper-agent/start.sh start.sh
RUN chmod +x start.sh
