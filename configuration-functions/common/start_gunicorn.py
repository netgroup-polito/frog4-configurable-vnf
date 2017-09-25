#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import os
import sys
from subprocess import call

from cf_core.config import Configuration
from cf_core.config_instance import ConfigurationInstance
from cf_core.management_interface_controller import ManagementInterfaceController
from cf_core.utils import check_validity_initial_params
from cf_core.cf_controller import ConfigFunctionsController

res = check_validity_initial_params(sys.argv)
if type(res) == str:
    error = res
    print(error)
    sys.exit(0)

configFunctionsController = ConfigFunctionsController()
managementInterfaceController = ManagementInterfaceController()
ConfigurationInstance().clear_db()

datadisk_path = res[1]
#configurationInstance.set_datadisk_path(datadisk_path)
ConfigurationInstance().save_datadisk_path(datadisk_path)
print("datadisk_path: " + datadisk_path)

# Check if datadisk exists and contains the right files
assert os.path.isdir(datadisk_path) is True, "datadisk not mounted into the VNF"
assert os.path.exists(datadisk_path + "/tenant-keys.json") is True, "Error, tenant-keys.json file not found in datadisk"
assert os.path.exists(datadisk_path + "/metadata.json") is True, "Error, metadata.json file not found in datadisk"
initial_configuration_path = datadisk_path + "/initial_configuration.json"
assert os.path.exists(initial_configuration_path) is True, "Error, initial_configuration.json file not found in datadisk"

# Push the initial configuration in order to configure the management interface
initial_configuration = None
with open(initial_configuration_path) as configuration:
    json_data = configuration.read()
    initial_configuration = json.loads(json_data)
configFunctionsController.set_management_interface(initial_configuration)

# Retrieve the assigned address of the management interface and start the rest server
name_iface_management = managementInterfaceController.get_name_management_interface()
address_iface_management = managementInterfaceController.get_interface_ipv4Configuration_address(name_iface_management)
rest_port = Configuration().REST_PORT
rest_address = "http://" + address_iface_management + ":" + rest_port
#configurationInstance.set_rest_address(rest_address)
ConfigurationInstance().save_rest_address(rest_address)

call("gunicorn -b " + address_iface_management + ':' + rest_port + " -t 500 main:app", shell=True)
