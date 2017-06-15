# frog4-configurable-vnf
This project collects Virtual Network Function images optimized for configuration purposes; in a nutshell each images is enriched with an agent, which is able to communicate with the frog4-configuration-service module exploiting the pub/sub paradigm.

Each configurable VNF is able to:
* interprete an high-level descripted configuration
* set the parameters described by the configuration into the VNF
* retrieve the actual status of the VNF
* describe the actual status of the VNF and export it to interested components (e.g., the configuration service)

