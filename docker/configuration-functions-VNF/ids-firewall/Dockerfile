FROM generic-image
MAINTAINER Politecnico di Torino

#########################################################################
#									#
#			Script boot					#
#									#
#########################################################################

# Copy the agent into the docker
RUN mkdir -p /configuration_agent
ADD ./ids-firewall-agent configuration_agent
RUN chmod +x configuration_agent/start_agent.sh

RUN mv ./configuration_agent/start.sh start.sh
RUN chmod +x start.sh
