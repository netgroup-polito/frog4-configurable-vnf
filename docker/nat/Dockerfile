FROM generic-image
MAINTAINER Politecnico di Torino

RUN apt-get update && apt-get install -y \ 
    iptables \
    bridge-utils \
    flex \
    bison 

RUN pip3 install --upgrade pip
RUN pip3 install python-iptables

# Copy and install agent's dependencies
RUN mkdir -p /dependencies

WORKDIR dependencies
RUN mkdir -p /conntrack-tools
WORKDIR conntrack-tools

RUN wget http://www.netfilter.org/projects/libnfnetlink/files/libnfnetlink-1.0.1.tar.bz2
RUN tar xvjf libnfnetlink-1.0.1.tar.bz2
WORKDIR libnfnetlink-1.0.1
RUN ./configure --prefix=/usr && make && make install
WORKDIR /dependencies/conntrack-tools

RUN wget https://www.netfilter.org/projects/libmnl/files/libmnl-1.0.4.tar.bz2
RUN tar xvjf libmnl-1.0.4.tar.bz2
WORKDIR libmnl-1.0.4
RUN ./configure --prefix=/usr && make && make install
WORKDIR /dependencies/conntrack-tools

RUN wget https://www.netfilter.org/projects/libnetfilter_conntrack/files/libnetfilter_conntrack-1.0.6.tar.bz2
RUN tar xvjf libnetfilter_conntrack-1.0.6.tar.bz2
WORKDIR libnetfilter_conntrack-1.0.6
RUN ./configure --prefix=/usr && make && make install
WORKDIR /dependencies/conntrack-tools

RUN wget https://www.netfilter.org/projects/libnetfilter_cttimeout/files/libnetfilter_cttimeout-1.0.0.tar.bz2
RUN tar xvjf libnetfilter_cttimeout-1.0.0.tar.bz2
WORKDIR libnetfilter_cttimeout-1.0.0
RUN ./configure --prefix=/usr && make && make install
WORKDIR /dependencies/conntrack-tools

RUN wget https://www.netfilter.org/projects/libnetfilter_cthelper/files/libnetfilter_cthelper-1.0.0.tar.bz2
RUN tar xvjf libnetfilter_cthelper-1.0.0.tar.bz2
WORKDIR libnetfilter_cthelper-1.0.0
RUN ./configure --prefix=/usr && make && make install
WORKDIR /dependencies/conntrack-tools

RUN wget https://www.netfilter.org/projects/libnetfilter_queue/files/libnetfilter_queue-1.0.2.tar.bz2
RUN tar xvjf libnetfilter_queue-1.0.2.tar.bz2
WORKDIR libnetfilter_queue-1.0.2
RUN ./configure --prefix=/usr && make && make install
WORKDIR /dependencies/conntrack-tools

RUN wget http://www.netfilter.org/projects/conntrack-tools/files/conntrack-tools-1.4.4.tar.bz2
RUN tar xvjf conntrack-tools-1.4.4.tar.bz2
WORKDIR conntrack-tools-1.4.4
RUN ./configure --prefix=/usr && make && make install
WORKDIR /dependencies/conntrack-tools

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


