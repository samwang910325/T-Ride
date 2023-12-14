import configparser
import os


class Config:
    config = configparser.ConfigParser()
    config.read('config.ini')

    def get(key):
        env_config = os.environ.get(key)
        return Config.config[key] if env_config is None else env_config
