class ConfigurationInstance(object):

    def __init__(self):
        self.db_file_path = "local_db.txt"


    def clear_db(self):
        open(self.db_file_path, 'w').close()


    def save_vnf_name(self, vnf_name):
        self._save_parameter("vnf_name", vnf_name)
    def get_vnf_name(self):
        return self._get_parameter("vnf_name")

    def save_nf_type(self, nf_type):
        self._save_parameter("nf_type", nf_type)
    def get_nf_type(self):
        return self._get_parameter("nf_type")

    def save_datadisk_path(self, datadisk_path):
        self._save_parameter("datadisk_path", datadisk_path)
    def get_datadisk_path(self):
        return self._get_parameter("datadisk_path")

    def save_on_change_interval(self, on_change_interval):
        self._save_parameter("on_change_interval", on_change_interval)
    def get_on_change_interval(self):
        return int(self._get_parameter("on_change_interval"))

    def save_iface_management(self, iface_management):
        self._save_parameter("iface_management", iface_management)
    def get_iface_management(self):
        return self._get_parameter("iface_management")

    def save_triple(self, triple):
        self._save_parameter("triple", triple)
    def get_triple(self):
        return self._get_parameter("triple")

    
    def _save_parameter(self, name, value):
        try:
            with open(self.db_file_path, 'a') as db_file:
                db_file.write(name + " " + str(value) + "\n")
                #db_file.truncate()
        except Exception as e:
            raise IOError("Error during the writing of file: " + self.db_file_path + "\n" + str(e))

    def _get_parameter(self, name):
        try:
            with open(self.db_file_path, 'r') as db_file:
                lines = db_file.readlines()
                db_file.close()
        except Exception as e:
            raise IOError("Error during the reading of file: " + self.db_file_path + "\n" + str(e))

        for line in lines:
            args = line.strip().split(' ')
            if args[0] == name:
                return args[1]

        return None


