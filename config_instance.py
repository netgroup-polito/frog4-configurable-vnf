class ConfigurationInstance(object):

    vnf = None
    #nf_type = None
    datadisk_path = None
    on_change_interval = None

    def get_vnf(self):
        return ConfigurationInstance.vnf
    def set_vnf(self, vnf):
        ConfigurationInstance.vnf = vnf

    def get_nf_type(self):
        with open('tmpFile', 'r') as file:
            nf_type = file.readlines()
        file.close
        return nf_type[0]
        #return ConfigurationInstance.nf_type
    def set_nf_type(self, nf_type):
        with open('tmpFile', 'w') as file:
            file.write(nf_type)
        file.close
        #ConfigurationInstance.nf_type = nf_type

    def get_datadisk_path(self):
        return ConfigurationInstance.datadisk_path
    def set_datadisk_path(self, datadisk_path):
        ConfigurationInstance.datadisk_path = datadisk_path

    def get_on_change_interval(self):
        return ConfigurationInstance.on_change_interval
    def set_on_change_interval(self, on_change_interval):
        ConfigurationInstance.on_change_interval = on_change_interval