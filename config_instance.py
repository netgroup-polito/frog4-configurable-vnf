class ConfigurationInstance(object):

    vnf = None
    nf_type = None
    datadisk_path = None

    def get_vnf(self):
        return ConfigurationInstance.vnf
    def set_vnf(self, vnf):
        ConfigurationInstance.vnf = vnf

    def get_nf_type(self):
        return ConfigurationInstance.nf_type
    def set_nf_type(self, nf_type):
        ConfigurationInstance.nf_type = nf_type

    def get_datadisk_path(self):
        return ConfigurationInstance.datadisk_path
    def set_datadisk_path(self, datadisk_path):
        ConfigurationInstance.datadisk_path = datadisk_path