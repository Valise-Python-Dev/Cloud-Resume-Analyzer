import yaml
import re

class SkillExtractor:
    def __init__(self, config_path="app/data_pipeline/config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

    def extract(self, text):
        skill_keywords = self.config["keywords"]["skills"]
        extracted = []

        for skill in skill_keywords:
            pattern = r"\b" + skill + r"\b"
            if re.search(pattern, text, re.IGNORECASE):
                extracted.append(skill)

        return list(set(extracted))
