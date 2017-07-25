FROM generic-image
MAINTAINER Politecnico di Torino


#########################################################################
#									#
#			Script boot					#
#									#
#########################################################################

RUN mkdir -p /libraries

#Install iperf3
WORKDIR libraries
RUN git clone https://github.com/esnet/iperf.git
WORKDIR iperf
RUN ./configure && make && make install && ldconfig

#install iperf3-python wrapper
WORKDIR libraries
RUN git clone https://github.com/thiezn/iperf3-python
WORKDIR iperf3-python
RUN python3 setup.py install

WORKDIR /

# Copy the agent into the docker
RUN mkdir -p /configuration_agent
WORKDIR configuration_agent
ADD ./iperf-agent/iperf iperf
ADD ./iperf-agent/common common
ADD ./iperf-agent/components components
ADD ./iperf-agent/vnf_template_library vnf_template_library
ADD ./iperf-agent/start_agent.sh start_agent.sh
RUN chmod +x start_agent.sh

WORKDIR /
ADD ./iperf-agent/start.sh start.sh
RUN chmod +x start.sh
