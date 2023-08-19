import os
from discopilot.configuration_loader import ConfigurationLoader

def test_load_ini_configuration():
    # Define path to the fake INI configuration file
    config_file_path = os.path.join(os.path.dirname(__file__), 'data', 'discopilot_config_template.ini')
    
    # Load configuration
    config = ConfigurationLoader.load_config(config_file_path)
    
    # Assertions to check the correctness of the loaded configuration

    # Twitter section
    assert 'Twitter' in config
    assert 'CONSUMER_KEY' in config['Twitter']
    assert 'CONSUMER_SECRET' in config['Twitter']
    assert 'ACCESS_TOKEN' in config['Twitter']
    assert 'ACCESS_TOKEN_SECRET' in config['Twitter']

    # Google section
    assert 'Google' in config
    assert 'PROJECT_ID' in config['Google']
    assert 'GOOGLE_APPLICATION_CREDENTIALS' in config['Google']

    # Discord section
    assert 'Discord' in config
    assert 'DISCORD_BOT_TOKEN' in config['Discord']
    assert 'INTERNAL_NEWS_CID' in config['Discord']
    assert 'CN_CID' in config['Discord']
    assert 'EN_CID' in config['Discord']
    assert 'ADMIN_ID' in config['Discord']
    assert 'SPECIFIC_REACTION' in config['Discord']
    assert 'COMMAND_PREFIX' in config['Discord']

    # ... You can add more assertions if you add more sections or keys to the INI file in the future.

def test_load_json_configuration():
    # Define path to the fake JSON configuration file
    config_file_path = os.path.join(os.path.dirname(__file__), 'data', 'discopilot_config_template.json')
    
    # Load configuration
    config = ConfigurationLoader.load_config(config_file_path)
    
    # Use the same assertions as before...
     # Twitter section
    assert 'Twitter' in config
    assert 'CONSUMER_KEY' in config['Twitter']
    assert 'CONSUMER_SECRET' in config['Twitter']
    assert 'ACCESS_TOKEN' in config['Twitter']
    assert 'ACCESS_TOKEN_SECRET' in config['Twitter']

    # Google section
    assert 'Google' in config
    assert 'PROJECT_ID' in config['Google']
    assert 'GOOGLE_APPLICATION_CREDENTIALS' in config['Google']

    # Discord section
    assert 'Discord' in config
    assert 'DISCORD_BOT_TOKEN' in config['Discord']
    assert 'ADMIN_ID' in config['Discord']
    assert 'SPECIFIC_REACTION' in config['Discord']
    assert 'COMMAND_PREFIX' in config['Discord']

def test_load_yaml_configuration():
    # Define path to the fake YAML configuration file
    config_file_path = os.path.join(os.path.dirname(__file__), 'data', 'discopilot_config_template.yml')
    
    # Load configuration
    config = ConfigurationLoader.load_config(config_file_path)
    
    # Use the same assertions as before...
     # Twitter section
    assert 'Twitter' in config
    assert 'CONSUMER_KEY' in config['Twitter']
    assert 'CONSUMER_SECRET' in config['Twitter']
    assert 'ACCESS_TOKEN' in config['Twitter']
    assert 'ACCESS_TOKEN_SECRET' in config['Twitter']

    # Google section
    assert 'Google' in config
    assert 'PROJECT_ID' in config['Google']
    assert 'GOOGLE_APPLICATION_CREDENTIALS' in config['Google']

    # Discord section
    assert 'Discord' in config
    assert 'DISCORD_BOT_TOKEN' in config['Discord']
    assert 'INTERNAL_NEWS_CID' in config['Discord']
    assert 'SPECIFIC_REACTION' in config['Discord']
    assert 'COMMAND_PREFIX' in config['Discord']