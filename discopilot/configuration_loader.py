import yaml
import json
import configparser
import os

class ConfigurationLoader:
    @staticmethod
    def load_config(config_file = None):
        """
        Load a configuration file.

        Args:
            config_file (str): The path to the configuration file. If not provided will run os.environ.get('DISCOPILOT_CONFIG')

        Returns:
            The configuration file as a dictionary.
        
        Example:
            config = ConfigurationLoader.load_config()
        """
        if config_file is None:
            config_file = os.environ.get('DISCOPILOT_CONFIG')
            if config_file is None:
                raise ValueError("config_file cannot be None")
            elif os.path.exists(config_file) is False:
                raise ValueError(f"config_file {config_file} does not exist")

        file_extension = os.path.splitext(config_file)[1]
        
        if file_extension == '.ini':
            config = configparser.ConfigParser()
            config.optionxform = lambda option: option
            config.read(config_file)
            return config
        elif file_extension == '.json':
            with open(config_file, 'r') as json_file:
                return json.load(json_file)
        elif file_extension in ['.yaml', '.yml']:
            with open(config_file, 'r') as yaml_file:
                return yaml.safe_load(yaml_file)
        else:
            raise ValueError(f"Unsupported configuration file type: {file_extension}")

