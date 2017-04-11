# Docker configurable VNFs

## How to build a configurable VNF

In this repository you will find 2 types of images:
* a generic configuration image (generic-configuration-image): it contains all the components needed by the VNF to communicate with the configuration service 
and to retrieve some essential information (e.g., URL of the message broker)
* specific network function images (e.g., DHCP or NAT): they are built starting from the generic-configuration-image, they are able to 
configure a specific network function and export their current state

Since the specific network function image is based on the generic-configuration-image, first you have to build the generic image
```sh
$ sudo docker build --tag="generic-configuration-agent" .
```
then you can build the specific image you need starting from the generic one (using the keyword 'FROM' into the Dockerfile)
```sh
$ sudo docker build --tag="nat_config" .
```
## How to create a configurable VNF
You can build your own VNF starting from the generic-configuration-image, which offers you:
* some basic libraries (YANG parsing and validation libraries, DoubleDecker, nano, net-tools)
* some generic feature (message bus communication, json validation against a YANG model)
* a generic library for Interface manipolation (you can include it with: from configuration_agent.common.interface import Interface)

In order to create your own VNF you have to write a plugin and a few scripts, which start the configuartion agent:
* create a class implementing the VNF interface you find into vnf_interface.py
* create a python script which instantiate the ConfigurationAgent class, passing your plugin class as parameter (e.g., if you develop a Dhcp class implementing the VNF interface, you may write a script like the following one, locating it in the Dhcp class file directory)
```python
from configuration_agent.agent import ConfigurationAgent
from configuration_agent.dhcp_server_config.dhcp_server import Dhcp

ConfigurationAgent(Dhcp)
```
* create a bash script called 'start.sh' which eventually starts services your VNF needs and executes the python script developed in the previous step (e.g., using the following line commands)
```python
sudo python3 -m configuration_agent.plugin_repository.agent_start.py
```
* create a Dockerfile starting from the one you find under the 'docker' directory (you have to start FROM the generic-configuration-agent image)
