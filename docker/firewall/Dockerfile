FROM generic-configuration-agent
MAINTAINER Politecnico di Torino

RUN apt-get update
RUN apt-get install -y iptables ebtables bridge-utils wget

RUN pip3 install netifaces python-iptables netaddr iptools jsonschema

#########################################################################
#									#
#			Script boot					#
#									#
#########################################################################

WORKDIR /configuration_agent
RUN mkdir firewall_config
ADD firewall_config firewall_config
RUN chmod +x firewall_config

#Insert template and the metadata file into the datadisk
ADD ./template.json /datadisk/template.json
ADD ./configuration_transparent_firewall_example.json /datadisk/initial_configuration.json
ADD ./metadata /datadisk/metadata

WORKDIR /
ADD ./start_firewall.sh start_firewall.sh
RUN chmod +x start_firewall.sh
ADD ./start_firewall_agent.sh start_firewall_agent.sh
RUN chmod +x start_firewall_agent.sh
ADD ./start.sh start.sh
RUN chmod +x start.sh




