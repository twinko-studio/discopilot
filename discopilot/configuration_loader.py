import yaml
import json
import configparser
import os

class ConfigurationLoader:
    @staticmethod
    def load_config(file_path):
        """
        Load a configuration file.

        Args:
            file_path (str): The path to the configuration file.

        Returns:
            The configuration file as a dictionary.
        
        Example:
            config_file = "/Users/tengfei/Code/key/config.ini"
            config = ConfigurationLoader.load_config(config_file)
        """
        file_extension = os.path.splitext(file_path)[1]
        
        if file_extension == '.ini':
            config = configparser.ConfigParser()
            config.read(file_path)
            return config
        elif file_extension == '.json':
            with open(file_path, 'r') as json_file:
                return json.load(json_file)
        elif file_extension in ['.yaml', '.yml']:
            with open(file_path, 'r') as yaml_file:
                return yaml.safe_load(yaml_file)
        else:
            raise ValueError(f"Unsupported configuration file type: {file_extension}")

