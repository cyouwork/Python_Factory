from ConfigParser import ConfigParser
class ConfigParser(ConfigParser):
    def optionxform(self, optionstr):
        return optionstr