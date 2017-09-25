from exception.wrong_configuration_file import WrongConfigurationFile
import configparser

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Configuration(object, metaclass=Singleton):

    def __init__(self):
        self.conf_file = "config/default-config.ini"

        self.inizialize()

    def inizialize(self):

        configParser = configparser.SafeConfigParser()
        configParser.read(self.conf_file)

        try:

            if configParser.has_option('logging', 'log_file'):
                self._LOG_FILE = configParser.get('logging', 'log_file')
            else:
                self._LOG_FILE = None
            self._LOG_LEVEL = configParser.get('logging', 'log_level')

            self._REST_PORT = configParser.get('rest_api', 'port')

        except Exception as ex:
            raise WrongConfigurationFile(str(ex))

    @property
    def LOG_FILE(self):
        return self._LOG_FILE

    @property
    def LOG_LEVEL(self):
        return self._LOG_LEVEL

    @property
    def REST_PORT(self):
        return self._REST_PORT