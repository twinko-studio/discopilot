from google.cloud import translate
from google.oauth2.service_account import Credentials


def create_translate_client():
    """
    Create a translate client to translate text based on the environment. If running on Google App Engine, no need to provide credentials. 
    If running elsewhere, use a JSON key file for credentials.

    Returns:
        translate.TranslationServiceClient: A translate client
    
    Examples:
    >>> create_translate_client()
    """
    # Check if running on Google App Engine
    if os.environ.get("IS_APP_ENGINE"):
        # Running on App Engine, no need to provide credentials
        client = translate.TranslationServiceClient()
    else:
        # Running elsewhere, use a JSON key file for credentials
        GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        trans_credentials = Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
        client = translate.TranslationServiceClient(credentials = trans_credentials)
    return client


def translate_text(text: str, target_language_code: str, parent: str, client) -> translate.Translation:  
    """
    Translate text to target language

    Args:
        text (str): The text to translate
        target_language_code (str): The target language code
        parent (str): The parent of the translation, in the format: projects/{project-id}
        client (translate.TranslationServiceClient): The translate client

    Returns:
        Transated text

    Examples:
    >>> client = create_translate_client()
    >>> translate_text("Hello, World!", "zh", "projects/1234567890", client = client)
    """
    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language_code,
    )
    return response.translations[0]

def translate_to_chinese(text, parent, client):
    """
    Translate text to chinese

    Args:
        text (str): The text to translate
        parent (str): The parent of the translation, in the format: projects/{project-id}
        client (translate.TranslationServiceClient): The translate client

    Returns:
        Transated text

    Examples:
    >>> client = create_translate_client()
    >>> translate_to_chinese("Hello, World!", parent = "projeect/12345", client = client)
    """
    result = translate_text(text, "zh", parent = parent, client = client)
    return result.translated_text
