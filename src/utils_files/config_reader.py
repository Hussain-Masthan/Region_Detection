import logging
import os
from configparser import ConfigParser

_logger = logging.getLogger(__name__)


class ConfigReader:

    def __init__(self):

        global config_mgr

    def config_reader(self):

        config_mgr = {}
        try:
            """ Get the information from Config File """
            config_mgr = ConfigParser()
            config_mgr.read(os.getcwd() + '/config/config.ini')
            _logger.info("Config File Reading process is completed")
        except Exception as e:
            _logger.error("Config File Reading Process is failed ! " + repr(e))

        return config_mgr
