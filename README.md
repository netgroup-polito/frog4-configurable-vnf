# frog4-configurable-vnf
This project collects Virtual Network Function images optimized for configuration purposes; in a nutshell each images is enriched with an agent, which is able to communicate with the frog4-configuration-service module exploiting the pub/sub paradigm.

Each configurable VNF is able to:
* interprete an high-level descripted configuration
* set the parameters described by the configuration into the VNF
* retrieve the actual status of the VNF
* describe the actual status of the VNF and export it to interested components (e.g., the configuration service)

##Datadisk
After a VNF deployment, the Universal Node attaches a volume (datadisk) containing some information needed by the configuration agent in order to work properly. 
The datadisk contains:
* the public key of the message broker
* both the private and the public key of VNF tenant
* the public key of the DD public tenant
* the template of the VNF
* an initial configuration, which the agent use in order to configure the VNF during the agent booting time (optional)
* a metadata file
Here you can find an example of metadata file (with the supported keyword)
