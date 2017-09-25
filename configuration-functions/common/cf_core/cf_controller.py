from cf_core.management_interface_controller import ManagementInterfaceController
from cf_core.nfs_controller import NfsController

class ConfigFunctionsController():

    def __init__(self):
        self.managementInterfaceController = ManagementInterfaceController()

    def set_management_interface(self, json_configuration):
        json_interface_management = json_configuration["configuration-functions:interface_management"]
        ManagementInterfaceController()
        self.managementInterfaceController.configure_management_interface(json_interface_management)

    def set_configuration(self, json_configuration):
        if 'configuration-functions:nfs' in json_configuration:
            json_nfs = json_configuration["configuration-functions:nfs"]
            NfsController().set_nfs(json_nfs)

    def get_full_status(self):

        status = {}

        name_management_interface = self.managementInterfaceController.get_name_management_interface()
        status["configuration-functions:interface_management"] = self.managementInterfaceController.get_interface(name_management_interface)
        status["configuration-functions:nfs"] = NfsController().get_nfs()

        return status









