FROM      generic-configuration-agent
MAINTAINER Politecnico di Torino

RUN apt-get update && apt-get install -y dnsmasq ssh iptraf

#Prepare the ssh server

RUN mkdir -p /var/run/sshd && mkdir -p /root/.ssh && echo 'root:root' | chpasswd
	
RUN echo "UseDNS no" >> /etc/ssh/sshd_config
RUN sed '/PermitRootLogin without-password/d' /etc/ssh/sshd_config > tmp_file && rm /etc/ssh/sshd_config && mv tmp_file /etc/ssh/sshd_config

RUN apt-get install -y isc-dhcp-server
ADD sysctl.conf /etc/sysctl.conf

RUN pip3 install netifaces netaddr iptools

#########################################################################
#									#
#			Script boot					#
#									#
#########################################################################
WORKDIR /configuration_agent
RUN mkdir dhcp_server_config
ADD dhcp_server_config dhcp_server_config
RUN chmod +x dhcp_server_config

WORKDIR / 
ADD ./start_dhcp.sh start_dhcp.sh
RUN chmod +x start_dhcp.sh
ADD ./start_dhcp_agent.sh start_dhcp_agent.sh
RUN chmod +x start_dhcp_agent.sh
ADD ./start.sh start.sh
RUN chmod +x ./start.sh
