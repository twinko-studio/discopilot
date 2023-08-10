from google.cloud import translate_v2 as translate
from discopilot.google.google_translate import create_translate_client, translate_text, translate_to_chinese

class TranslateBot:
    """
    A bot that interacts with Google Translate.

    Attributes:
        translate_client (translate.Client): A Google Cloud Translate client.

    Example:
        google_project_id = 'projects/my_project/locations/my_location'
        translate_bot = TranslateBot(google_project_id)
        translated_text = translate_bot.translate_text("Hello, World!", "es")
        print(translated_text)  # Output in Spanish
        translated_text = translate_bot.translate_to_chinese("Hello, World!")
        print(translated_text)  # Output in Chinese
    """

    def __init__(self, google_project_id):
        """
        Initialize the TranslateBot with the Google Project ID.

        Args:
            google_project_id (str): The Google Cloud Project ID.
        """
        # Google Translate parent resource
        assert google_project_id
        self.parent = f"projects/{google_project_id}"
        self.client = create_translate_client()

    def translate_text(self, text, target_language_code, parent):
        """
        Translate text into the specified target language using Google Translate.

        Args:
            text (str): The text to be translated.
            target_language_code (str): The target language code (e.g., 'en', 'es').

        Returns:
            translate.Translation: A Translation object containing the translated text.

        Example:
            translated_text = translate_bot.translate_text("Hello, World!", "zh")
        """
        translate_text(client = self.client, text = text, target_language_code = target_language_code, parent = self.parent)

    def translate_to_chinese(text):
        """
        Translate text into Chinese.

        Args:
            text (str): The text to be translated.
            client (translate.Client): A Google Cloud Translate client.

        Returns:
            translate.Translation: A Translation object containing the translated text.

        Example:
            translated_text = translate_to_chinese("Hello, World!", translate_client)
        """
        return translate_to_chinese(client = self.client, text = text, target_language_code = "zh", parent = self.parent)
