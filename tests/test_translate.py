from google.cloud import translate_v2 as translate
from discopilot.google.google_translsate import create_translate_client, translate_text, translate_to_chinese
from discopilot.bot.translate import TranslateBot

google_project_id = 'rss-trigger'
translate_bot = TranslateBot(google_project_id)
translate_bot.translate_text("Hello, World!", "es")
translate_bot.translate_to_chinese("Hello, World!")

