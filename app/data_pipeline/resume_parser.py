import spacy

class ResumeParser:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract_entities(self, text):
        doc = self.nlp(text)
        entities = {
            "names": [],
            "organizations": [],
            "locations": []
        }

        for ent in doc.ents:
            if ent.label_ == "PERSON":
                entities["names"].append(ent.text)
            elif ent.label_ in ["ORG"]:
                entities["organizations"].append(ent.text)
            elif ent.label_ in ["GPE"]:
                entities["locations"].append(ent.text)

        return entities
