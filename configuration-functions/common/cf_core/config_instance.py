class ConfigurationInstance(object):

    def __init__(self):
        self.db_file_path = "local_db.txt"


    def clear_db(self):
        open(self.db_file_path, 'w').close()


    def save_datadisk_path(self, datadisk_path):
        self._save_parameter("datadisk_path", datadisk_path)
    def get_datadisk_path(self):
        return self._get_parameter("datadisk_path")

    def save_rest_address(self, rest_address):
        self._save_parameter("rest_address", rest_address)
    def get_rest_address(self):
        return self._get_parameter("rest_address")

    def save_name_management_interface(self, name_management_interface):
        self._save_parameter("name_management_interface", name_management_interface)
    def get_name_management_interface(self):
        return self._get_parameter("name_management_interface")


    def _save_parameter(self, name, value):
        try:
            with open(self.db_file_path, 'a') as db_file:
                db_file.write(name + " " + value + "\n")
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



