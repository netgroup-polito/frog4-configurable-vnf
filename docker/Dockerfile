FROM      generic-configuration-agent
MAINTAINER Politecnico di Torino

RUN apt-get update && apt-get install -y iptables
RUN pip3 install netifaces netaddr iptools jsonschema

###############
#
# ADD HERE ALL THE DEPENDENCY OF YOUR PLUGIN
#
###############


#Insert template and the metadata file into the datadisk
WORKDIR /datadisk
ADD template.json template.json
ADD metadata metadata
ADD initial_configuration.json initial_configuration.json

#Move the specific VNF plugin into the configuration_agent directory
WORKDIR /configuration_agent
RUN mkdir dhcp_server_config
ADD dhcp_server_config dhcp_server_config
RUN chmod +x dhcp_server_config

#Add start.sh (the UN expects such a script to exist) and other scripts it executes
WORKDIR /
ADD ./start_dhcp.sh start_dhcp.sh
RUN chmod +x start_dhcp.sh
ADD ./start_dhcp_agent.sh start_dhcp_agent.sh
RUN chmod +x start_dhcp_agent.sh
ADD ./start.sh start.sh
RUN chmod +x ./start.sh