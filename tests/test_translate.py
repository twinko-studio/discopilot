from google.cloud import translate_v2 as translate
from discopilot.google.google_translsate import create_translate_client, translate_text, translate_to_chinese
from discopilot.bot.translate import TranslateBot

## Get project ID
PROJECT_ID = os.environ.get('PROJECT_ID')

## Lower level function
client = create_translate_client()
tt = translate_text("Hello, World!", "zh", PROJECT_ID, client = client)
print(tt.translated_text)
tt = translate_to_chinese("Hello, World!", PROJECT_ID, client = client)
print(tt)

## TranslateBot Class: easy API
translate_bot = TranslateBot(PROJECT_ID)
tt = translate_bot.translate_text(text = "Hello, World!", target_language_code = "zh")
print(tt.translated_text)
translate_bot.translate_to_chinese("Hello, World!")

