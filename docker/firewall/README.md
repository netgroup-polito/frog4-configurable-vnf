## Docker-based firewall VNF

This file contains the instructions to build a Docker network function that includes a firewall based on iptables.

### Configuring iptables

The configuration of iptables has to be embedded in the Docker itself; right now, we cannot change dynamically (at run-time) the configuration.

To change the configuration of the firewall (e.g., changing the network interfaces it binds to, the rules used to allow/block the traffic, etc.), edit the file `start.sh`.
This file will be pushed automatically in the Docker image, once created, and will be executed at the startup of the VNF.

### Creating the Docker image

Now you can create the Docker image with the firewall by launching the following command:

    sudo docker build --tag="firewall" .

This will create the Docker image starting from the base image specified in `Dockerfile`; the new image is stored in the Docker default folder on your filesystem (localhost).

If you want to be more generic and publish the Docker image in a (public or private) repository, you can use the following command:

    sudo docker build --tag="localhost:5000/firewall" .
    docker push localhost:5000/firewall

This will register your VNF named `firewall` in the local registry (given by the the string `localhost:5000`), which has to be up and running on localhost.


