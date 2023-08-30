import os
from discopilot.configuration_loader import ConfigurationLoader
import requests

def get_twitter_creds(config_file):
    config = ConfigurationLoader.load_config(config_file)
    return {
        'consumer_key': config['Twitter']['CONSUMER_KEY'],
        'consumer_secret': config['Twitter']['CONSUMER_SECRET'],
        'access_token': config['Twitter']['ACCESS_TOKEN'],
        'access_token_secret': config['Twitter']['ACCESS_TOKEN_SECRET'],
    }   

def get_google_translate_details(config_file):
    config = ConfigurationLoader.load_config(config_file)
    return {
        'project_id': config['Google']['PROJECT_ID'],
        'credentials_file': os.path.expanduser(config['Google']['GOOGLE_APPLICATION_CREDENTIALS']),
    }   

def get_discord_details(config_file):
    config = ConfigurationLoader.load_config(config_file)
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
    filename = os.path.expanduser(filename)
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

def hf_text_post(text, model_id, **kwargs):
    API_URL = get_hf_api(model_id)
    headers = get_hf_headers()
    payload = {"inputs": text, "parameters": kwargs}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response

def get_summary_from_response(response):

    json_response = response.json()

    if response.status_code != 200:
        print(f"Request failed with status code {response.status_code}: {response.text}")
        return ""

    if isinstance(json_response, list) and len(json_response) > 0:
        if 'summary_text' in json_response[0]:
            return json_response[0]['summary_text']
        else:
            print("No summary_text in the first item of the response.")
            return ""
    elif isinstance(json_response, dict) and 'summary_text' in json_response:
        return json_response['summary_text']
    else:
        print("Unexpected response structure.")
        return ""

