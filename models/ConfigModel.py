# coding:utf-8
import configparser
import os


class ConfigModel:
    test = os.path.abspath(__file__)

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + '/../'
    DATA_DIR = ROOT_DIR + 'data/'
    LOGS_DIR = ROOT_DIR + 'logs/'
    MODELS_DIR = ROOT_DIR + 'models/'

    __CONFIG_FILE = 'config.ini'
    __config_parser = None

    @classmethod
    def __get_config_parser(cls):
        if cls.__config_parser is None:
            cls.__config_parser = configparser.ConfigParser()
            cls.__config_parser.read(ConfigModel.__CONFIG_FILE)
        return ConfigModel.__config_parser

    @classmethod
    def get_chrome_driver_path(cls):
        return cls.ROOT_DIR + ConfigModel.__get_config_parser().get('require', 'chrome_driver_name')

    @classmethod
    def get_end_point_url(cls):
        return cls.__get_config_parser().get('common', 'endpoint_url')

    @classmethod
    def get_user_email(cls):
        return cls.__get_config_parser().get('secure', 'user_email')

    @classmethod
    def get_password(cls):
        return cls.__get_config_parser().get('secure', 'password')

