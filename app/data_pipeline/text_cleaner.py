import yaml
from .utils import (
    remove_email, remove_url,
    remove_special_chars, remove_extra_spaces
)

class TextCleaner:
    def __init__(self, config_path="app/data_pipeline/config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

    def clean(self, text):
        cfg = self.config["cleaning"]

        if cfg["remove_emails"]:
            text = remove_email(text)

        if cfg["remove_urls"]:
            text = remove_url(text)

        if cfg["remove_special_chars"]:
            text = remove_special_chars(text)

        if cfg["remove_extra_spaces"]:
            text = remove_extra_spaces(text)

        return text
