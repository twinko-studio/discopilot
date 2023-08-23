from transformers import pipeline
from discopilot.utils import get_hf_headers, get_hf_api
import requests

class Summarizer:
    def __init__(self, model_id, **kwargs):
        self.model_id = model_id

    def summarize(self, text, **kwargs):
        raise NotImplementedError("Subclasses should implement this!")


class HuggingFaceSummarizer(Summarizer):
    def summarize(self, text, model_id = "facebook/bart-large-cnn", env = "inference_api",
                  max_length=500, min_length=100, do_sample=False, **kwargs):
        self.model_id = model_id
        if env == "inference_api":
            print("using inference API")
            API_URL = get_hf_api(model_id)
            headers = get_hf_headers()
            payload = {"inputs": text,
                        "parameters": {
                            "max_length" : max_length,
                            "min_length" : min_length,
                            "do_sample": do_sample}}
            response = requests.post(API_URL, headers=headers, json=payload)

            json_response = response.json()

            print("response code", response.status_code)

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

        elif env == "local":
            prnit("using local model")
            summarizer = pipeline("summarization", model=self.model_id)
            return summarizer(text, max_length=max_length, min_length=min_length, do_sample=do_sample, **kwargs)
        else:
            raise ValueError(f"env {env} not supported!")


def create_summarizer(platform, model_id,  **kwargs):
    if platform == "huggingface":
        return HuggingFaceSummarizer(model_id = model_id, **kwargs)
    else:
        raise ValueError(f"Platform {platform} not supported!")


def summarize(text, model_id="facebook/bart-large-cnn", platform="huggingface", env = "inference_api", **kwargs):
    """
    Summarize text using the specified model and platform.

    Args:
        text (str): The text to summarize.
        model (str): The model to use for summarization.
        platform (str): The platform to use for summarization.
        env (str): The environment to use for summarization. "inference_api" (huggingface) or "local".

    Returns:
        str: The summarized text.

    Examples:
        >>> summarize("This is a test", model="facebook/bart-large-cnn", platform="huggingface")
    """
    summarizer = create_summarizer(platform, model_id = model_id, **kwargs)
    print("summarizing...")
    return summarizer.summarize(text)
