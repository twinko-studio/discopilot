from discopilot.utils import hf_text_post

#from transformers import pipeline

class Espresso:
    def __init__(self, model_id, **kwargs):
        self.model_id = model_id

    def press(self, text, **kwargs):
        raise NotImplementedError("Subclasses should implement this!")


class HuggingFaceEspresso(Espresso):
    def press(self, text, model_id = "facebook/bart-large-cnn", env = "inference_api",
                  max_length=500, min_length=100, do_sample=False, **kwargs):
        self.model_id = model_id
        if env == "inference_api":
            print("using inference API")
            response = hf_text_post(text = text, model_id = model_id, max_length=500, min_length=100, do_sample=False, **kwargs)
            
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



def espresso(model_id="facebook/bart-large-cnn", platform="huggingface", env="inference_api", **kwargs):
    """
    Summarize text using the specified model and platform.

    Example:
    from discopilot.utils import read_content_from_file
    article = read_content_from_file("~/Code/twinko-studio/discopilot/tests/data/article.txt")
    esp = espresso()
    esp.press(article)
    # the same as default
    esp = espresso(model_id="facebook/bart-large-cnn", platform="huggingface", env="inference_api")
    esp.press(article)
    """
    if platform == "huggingface":
        return HuggingFaceEspresso(model_id = model_id, **kwargs)
    else:
        raise ValueError(f"Platform {platform} not supported!")

