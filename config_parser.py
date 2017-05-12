import configparser

class ConfigParser():

    config_file = "config/default-config.ini"

    def __init__(self):
        self.parser = configparser.SafeConfigParser()

    def get(self, section, key):
        self.parser.read(self.config_file)
        return self.parser.get(section, key)

    def add_section(self, section):
        self.parser.add_section(section)

    def set(self, section, key, value):
        self.parser.set(section, key, value)

    def write(self):
        with open(self.config_file, 'a') as configfile:
            self.parser.write(configfile)