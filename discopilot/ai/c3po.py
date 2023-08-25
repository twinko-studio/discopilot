from discopilot.utils import get_google_translate_details
from discopilot.configuration_loader import ConfigurationLoader
from discopilot.google.google_translate import create_translate_client, translate_text, translate_to_chinese


class C3PO:
    def translate(self, text, target_lang, **kwargs):
        raise NotImplementedError("Subclasses must implement the `translate` method")
    def list_languages(self):
        raise NotImplementedError("Subclasses must implement the `list_languages` method")


class HuggingFaceC3PO(C3PO):
    def __init__(self, model_id, env = "inference_api"):
        self.model_id = model_id

    def translate(self, text, source_lang, target_lang, **kwargs):
        assert source_lang
        assert target_lang

        model_id = f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"
        response = hf_text_post(text = text, model_id = model_id, **kwargs)
        return response
    
    def translate_to_chinese(self, text):
        response = self.translate(text = text, source_lang="en", target_lang="zh")
        return response

class GoogleCloudC3PO(C3PO):

    def __init__(self, project_id, credentials_file):
        """
        Initialize the TranslateBot with the Google Project ID.
        """
        # Google Translate parent resource
        if not credentials_file:
            config = ConfigurationLoader.load_config()
            google_translate_details = get_google_translate_details(config)
            credentials_file = google_translate_details['credentials_file']
            project_id = google_translate_details['project_id']

        assert project_id
        assert credentials_file

        self.project_id = project_id
        self.client = create_translate_client(credentials_file)
        self.clientv2 = create_translate_client(credentials_file, version="v2")

    def list_languages(self) -> dict:
        """Lists all available languages."""
        results = self.clientv2.get_languages()

        for language in results:
            print(f"{language['name']:20} ({language['language']})")

        ## return results

    def list_languages_with_target(self, target: str) -> dict:
        """Lists all available languages and localizes them to the target language.

        Target must be an ISO 639-1 language code.
        See https://g.co/cloud/translate/v2/translate-reference#supported_languages
        """

        results = self.clientv2.get_languages(target_language=target)

        for language in results:
            print(f"{language['name']:20} ({language['language']})")

        ## return results

    def translate(self, text, target_lang, **kwargs):
        """
        Translate text into the specified target language using Google Translate.
        """
        res = translate_text(client = self.client, text = text, 
                           target_language_code = target_lang, project_id = self.project_id)

        return res.translated_text

    def translate_to_chinese(self, text):
        """
        Translate text into Chinese.
        """
        res = translate_to_chinese(text = text,  project_id = self.project_id, client = self.client)

        return res

    def detect_language(self, text: str):
        PARENT = f"projects/{self.project_id}"
        response = self.client.detect_language(parent=PARENT, content=text)
        return response.languages[0]


def c3po(engine = "google", model_id = None, project_id = None, credentials_file = None):
    """
    Create the C-3PO Translator object using the specified platform and model.

    Args:
        engine (str): The translation engine to use. Currently supports "google" and "huggingface".
        model_id (str): The model ID to use. Only required for HuggingFace.
        project_id (str): The Google Cloud project ID. Only required for Google Cloud.
        credentials_file (str): The path to the Google Cloud credentials file. Only required for Google Cloud.

    Returns:
        A Translator object.

    Examples:
    >>> c3pobot = c3po()
    >>> c3pobot.translate_to_chinese("Hello, World!")
    >>> c3pobot.translate("Hello, World!", target_lang="zh")
    >>> c3pobot.detect_language("Hello, World!")
    >>> c3pobot.list_languages()
    >>> c3pobot.list_languages_with_target("zh")
    """ 

    if engine == "huggingface":
        if model_id is None:
            model_id = "Helsinki-NLP/opus-mt-en-zh"
        return HuggingFaceC3PO(model_id)
    elif engine == "google":
        return GoogleCloudC3PO(project_id, credentials_file)
    else:
        raise ValueError(f"engine {engine} not supported!")


