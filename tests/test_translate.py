from google.cloud import translate_v2 as translate
from discopilot.google.google_translsate import create_translate_client, translate_text, translate_to_chinese
from discopilot.bot.translate import TranslateBot
import configparser

## Get project ID
config_file = '/Users/tengfei/Code/key/config.ini'
config = configparser.ConfigParser()
config.read(config_file)
PROJECT_ID = config['Google']['PROJECT_ID']

## Lower level function
client = create_translate_client(config_file=config_file)
tt = translate_text("Hello, World!", "zh", PROJECT_ID, client = client)
print(tt.translated_text)
tt = translate_to_chinese("Hello, World!", PROJECT_ID, client = client)
print(tt)

## TranslateBot Class: easy API
translate_bot = TranslateBot(project_id = PROJECT_ID, config_file=config_file)
tt = translate_bot.translate_text(text = "Hello, World!", target_language_code = "zh")
print(tt.translated_text)
translate_bot.translate_to_chinese("Hello, World!")

