# VNF Template Library

This library models the VNF template used by the frog-orchestrator. Every VNF is described in terms of infrastructure and in terms of configuration. Going into details a template describes a VNF through the following parameters:
  * Type of the VNF
  * Image URI (not needed in some cases)
  * YANG model URI (not needed in some cases)
  * Amount of memory
  * CPU requirements (platform type, number of cores etc)
  * List of ports
  
For each port is possibile to specify additional parameters such as the number and the label and also ipv4 or ipv6 configurations, if present.

This library is Python 2/3 compatible and is referenced as a submodule in all projects that use it.
