FROM ubuntu
MAINTAINER Politecnico di Torino

RUN apt-get update && apt-get install -y ssh 

#Prepare the ssh server
RUN mkdir -p /var/run/sshd && mkdir -p /root/.ssh && echo 'root:root' | chpasswd
	
#RUN echo "UseDNS no" >> /etc/ssh/sshd_config
#RUN sed '/PermitRootLogin without-password/d' /etc/ssh/sshd_config > tmp_file && rm /etc/ssh/sshd_config && mv tmp_file /etc/ssh/sshd_config

ENV TERM xterm
#Install tools to debug and management, xterm variable required in order to run nano
RUN apt-get update && apt-get install -y \
    htop \
    net-tools \
    nano \
    vim \
    iputils-ping \
    tcpdump \
    wget 
    
RUN mv /usr/sbin/tcpdump /usr/bin/tcpdump

RUN apt-get update && apt-get install -y \
    python3-setuptools \
    python3-pip \
    libffi-dev \
    git \
    sudo 

#RUN git clone https://github.com/pyca/pynacl.git
#WORKDIR pynacl
#RUN python3 setup.py install

WORKDIR /
RUN pip3 install --upgrade pip
RUN pip3 install aiozmq  
RUN pip3 install zmq
RUN pip3 install pyang
RUN apt-get install -y xsltproc
RUN apt-get install -y jing
RUN pip3 install xmltodict
RUN pip3 install netifaces
RUN pip3 install jsonschema
RUN pip3 install flask
RUN pip3 install flask-restplus

RUN pip3 install PyNaCl
RUN pip3 install pyzmq
RUN pip3 install tornado
RUN pip3 install cffi
RUN pip3 install urwid

RUN git clone https://github.com/Acreo/DoubleDecker-py.git
WORKDIR DoubleDecker-py
RUN git reset --hard c74e81defac1dcb093dd2151c3ce48a6e4fa7750
RUN python3 setup.py install
RUN mkdir /etc/doubledecker

WORKDIR /


