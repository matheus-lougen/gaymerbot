import os
import yaml
import logging

from .logger import Logger


class Config():

    def __init__(self, path):
        logger = Logger()
        logger.setup_formatters()
        self.log = logger.setup_logger('config', debug_mode=False, file_level=logging.INFO, stream_level=logging.INFO)

        if not os.path.exists(path):
            self.log.critical(f'Could not find a valid config file at: {path}')
            return
        else:
            try:
                with open(path, 'r') as file:
                    config = yaml.safe_load(file)
            except Exception as e:
                self.log.critical('An exception ocurred while reading the config file')
                self.log.exception(e)
                return
            else:
                for key in config:
                    setattr(self, key, config[key])
