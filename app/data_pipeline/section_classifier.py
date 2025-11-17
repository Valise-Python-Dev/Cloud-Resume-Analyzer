import re

class SectionClassifier:
    def classify(self, text):
        sections = {
            "education": "",
            "experience": "",
            "skills": "",
            "projects": "",
            "certifications": ""
        }

        current_section = None
        lines = text.split("\n")

        for line in lines:
            line_lower = line.lower()

            if "education" in line_lower:
                current_section = "education"
            elif "experience" in line_lower or "work history" in line_lower:
                current_section = "experience"
            elif "skills" in line_lower:
                current_section = "skills"
            elif "project" in line_lower:
                current_section = "projects"
            elif "certification" in line_lower:
                current_section = "certifications"

            if current_section:
                sections[current_section] += line + "\n"

        return sections
