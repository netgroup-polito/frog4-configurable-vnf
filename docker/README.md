#Docker configurable VNF
##How to build a configurable VNF
In this repository you will find 2 types of images:
* a generic-configuration-image: it contains all the stuffs that the VNF needs in order to communicate with the configuration service 
and to retrieve some essential information (e.g., message broker url)
* specific network function images (e.g., DHCP or NAT): they are built starting from the generic-configuration-image, they are able to 
configure a specific network function and export their actual state

Since the specific network function image is based on the generic-configuration-image, first you have to build the generic image
```sh
$ sudo docker build --tag="generic-agent-image" .
```
then you can build the specific image you need specifying the tag of the generic image you have chose
```sh
$ sudo docker build --tag="nat_config" --build-arg generic-image=generic-agent-image .
```
