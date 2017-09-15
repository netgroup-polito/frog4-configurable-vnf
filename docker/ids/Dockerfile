FROM generic-image
MAINTAINER Politecnico di Torino

RUN apt-get update && apt-get install -y \
    openssh-server \
    ethtool \
    build-essential \
    flex \
    bison \
    libpcap-dev \
    libpcre3 \
    libpcre3-dev \
    libdumbnet-dev \
    liblzma-dev \
    zlib1g-dev \
    openssl \
    libssl-dev \
    bridge-utils

RUN pip3 install --upgrade pip
RUN pip3 install idstools

RUN wget https://www.snort.org/downloads/snort/daq-2.0.6.tar.gz
RUN tar xvfz daq-2.0.6.tar.gz
WORKDIR daq-2.0.6
RUN ./configure && make && sudo make install
WORKDIR /

RUN wget https://www.snort.org/downloads/snort/snort-2.9.9.0.tar.gz
RUN tar xvfz snort-2.9.9.0.tar.gz
WORKDIR snort-2.9.9.0
RUN ./configure --enable-sourcefire && make && sudo make install
WORKDIR /

RUN ldconfig
RUN ln -s /usr/local/bin/snort /usr/sbin/snort

#########################################################################
#									#
#			Script boot					#
#									#
#########################################################################

ADD ./snort.conf my_snort.conf
ADD ./start.sh start.sh
RUN chmod +x start.sh