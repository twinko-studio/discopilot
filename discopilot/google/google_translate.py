from google.cloud import translate
from google.oauth2.service_account import Credentials
import os
import configparser


def create_translate_client(credentials_file: str):
    """
    Create a translate client to translate text based on the environment. If running on Google App Engine, no need to provide credentials. 
    If running elsewhere, use a JSON key file for credentials.

    Args:
        credentials_file (str): The path of your JSON key file
    Returns:
        translate.TranslationServiceClient: A translate client
    
    Examples:
    >>> create_translate_client()
    """
    # Check if running on Google App Engine, set this environment variable in app.yaml or other environment configuration
    if os.environ.get("IS_APP_ENGINE"):
        # Running on App Engine, no need to provide credentials
        client = translate.TranslationServiceClient()
    else:
        if not credentials_file:
            raise Exception("Please provide the path of your JSON key file.")
        trans_credentials = Credentials.from_service_account_file(credentials_file)
        client = translate.TranslationServiceClient(credentials = trans_credentials)
    return client


def translate_text(text: str, target_language_code: str, project_id: str, client) -> translate.Translation:  
    """
    Translate text to target language

    Args:
        text (str): The text to translate
        target_language_code (str): The target language code
        project_id: The project ID of google cloud
        client (translate.TranslationServiceClient): The translate client

    Returns:
        Transated text

    Examples:
    >>> client = create_translate_client()
    >>> translate_text("Hello, World!", "zh", "project/1234567890", client = client)
    """
    assert project_id
    parent = f"projects/{project_id}"
    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language_code,
    )
    return response.translations[0]

def translate_to_chinese(text, project_id, client):
    """
    Translate text to chinese

    Args:
        text (str): The text to translate
        project_id (str): The project ID of google cloud
        client (translate.TranslationServiceClient): The translate client

    Returns:
        Transated text

    Examples:
    >>> client = create_translate_client()
    >>> translate_to_chinese("Hello, World!", porject_id = "12345", client = client)
    """
    result = translate_text(text= text, target_language_code = "zh", project_id = project_id, client = client)
    return result.translated_text
