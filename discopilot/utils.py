import os
from discopilot.configuration_loader import ConfigurationLoader

def get_twitter_creds(config):
    return {
        'consumer_key': config['Twitter']['CONSUMER_KEY'],
        'consumer_secret': config['Twitter']['CONSUMER_SECRET'],
        'access_token': config['Twitter']['ACCESS_TOKEN'],
        'access_token_secret': config['Twitter']['ACCESS_TOKEN_SECRET'],
    }   

def get_google_translate_details(config):
    return {
        'project_id': config['Google']['PROJECT_ID'],
        'credentials_file': os.path.expanduser(config['Google']['GOOGLE_APPLICATION_CREDENTIALS']),
    }   

def get_discord_details(config):
    return {
        'token': config['Discord']['DISCORD_BOT_TOKEN'],
        'dev_token': config['Discord']['DISCORD_BOT_DEV_TOKEN'],
        'guild_id': config['Discord']['TS_GUILD_ID'],
        'admin_id': config['Discord']['ADMIN_ID'],
        'emoji_id': config['Discord']['SPECIFIC_REACTION'],
        'command_prefix': config['Discord']['COMMAND_PREFIX'],
        'channel_ids' : config['Discord_CID'],
        'channel_mapping': config['Channel_Mapping'],
        'chinese_mapping': config['Chinese_Mapping'],
        'channel_quotas': config['Channel_Quotas']
    }

def read_content_from_file(filename):
    with open(filename, 'r') as file:
        return file.read()

def get_hf_headers():
    config = ConfigurationLoader.load_config()
    hf_token = config['HuggingFace']['ACCESS_TOKEN']
    headers = {"Authorization": f"Bearer {hf_token}"}
    return headers

def get_hf_api(model_id):
    API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
    return API_URL