from discopilot.utils import hf_text_post, read_content_from_file, get_summary_from_response
import os
from transformers import pipeline

class Espresso:
    def __init__(self, model_id, **kwargs):
        self.model_id = model_id

    def press(self, text, **kwargs):
        raise NotImplementedError("Subclasses should implement this!")


class HuggingFaceEspresso(Espresso):
    def press(self, text, model_id = "facebook/bart-large-cnn", env = "inference_api",
                  max_length=500, min_length=100, do_sample=False, **kwargs):
        self.model_id = model_id
        
        # write a functino to tell if a string is existing file
        # if it is, read the content from the file
        # if not, treat it as a string
        if isinstance(text, str):
            if os.path.isfile(os.path.expanduser(text)):
                text = read_content_from_file(text)


        if env == "inference_api":
            print("Using HuggingFace inference API:\n")
            response = hf_text_post(text = text, model_id = model_id, max_length=max_length, min_length=min_length, do_sample=do_sample, **kwargs)
            res = get_summary_from_response(response)
            return res


        elif env == "local":
            print("using local model")
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
    # this is equivalent to:
    esp = espresso(model_id="facebook/bart-large-cnn", platform="huggingface", env="inference_api")
    esp.press(article)
    # this is equivalent to:
    esp.press("~/Code/twinko-studio/discopilot/tests/data/article.txt")
    """
    if platform == "huggingface":
        return HuggingFaceEspresso(model_id = model_id, **kwargs)
    else:
        raise ValueError(f"Platform {platform} not supported!")

