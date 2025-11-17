from .file_loader import FileLoader
from .text_cleaner import TextCleaner
from .resume_parser import ResumeParser
from .section_classifier import SectionClassifier
from .skill_extractor import SkillExtractor

class PreprocessPipeline:
    def __init__(self, file_path):
        self.file_path = file_path
        self.loader = FileLoader(file_path)
        self.cleaner = TextCleaner()
        self.parser = ResumeParser()
        self.classifier = SectionClassifier()
        self.skill_extractor = SkillExtractor()

    def run(self):
        raw_text = self.loader.load()
        clean_text = self.cleaner.clean(raw_text)

        sections = self.classifier.classify(clean_text)
        skills = self.skill_extractor.extract(clean_text)
        entities = self.parser.extract_entities(clean_text)

        return {
            "clean_text": clean_text,
            "sections": sections,
            "skills": skills,
            "entities": entities
        }
