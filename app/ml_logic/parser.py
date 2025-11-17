import re
from typing import List, Dict, Any
import spacy

# load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    # Fallback if model isn't found, though you already installed it
    print(f"Warning: spacy model not found: {e}")
    nlp = spacy.blank("en")

SKILLS_SEED = [
    "python", "java", "c++", "c", "tensorflow", "pytorch", "scikit-learn",
    "docker", "kubernetes", "aws", "gcp", "azure", "nlp", "computer vision",
    "pandas", "numpy", "sql", "nosql", "react", "nodejs", "git", "rest",
    "fastapi", "flask", "django", "html", "css", "javascript"
]

EMAIL_RE = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
PHONE_RE = re.compile(r"(\+?\d{1,4}[\s\-]?)?(\(?\d{2,4}\)?[\s\-]?)?[\d\s\-]{6,12}")
DATE_RANGE_RE = re.compile(r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|'
                           r'January|February|March|April|May|June|July|August|September|October|November|December|\d{4})'
                           r'[^,\n\r]{0,30}(?:\d{4}))', re.IGNORECASE)
SECTION_HEADERS = ["experience", "work experience", "professional experience",
                   "education", "skills", "projects", "certifications", "summary", "objective"]

def extract_emails(text: str) -> List[str]:
    return list(set(m.group(0) for m in EMAIL_RE.finditer(text)))

def extract_phones(text: str) -> List[str]:
    phones = []
    for m in PHONE_RE.finditer(text):
        phones.append(m.group(0).strip())
    return list(dict.fromkeys(phones))

def extract_skills(text: str, skills_seed: List[str] = SKILLS_SEED) -> List[str]:
    text_low = text.lower()
    found = set()
    for s in skills_seed:
        if s.lower() in text_low:
            found.add(s)
    return sorted(found)

def split_into_sections(text: str) -> Dict[str, str]:
    lines = [l.strip() for l in text.splitlines()]
    sections = {}
    current = "header"
    buffer = []
    for l in lines:
        low = l.lower().strip(':').strip()
        if len(l) == 0:
            if buffer:
                sections.setdefault(current, "")
                sections[current] += "\n".join(buffer) + "\n"
                buffer = []
            continue
        if any(h in low for h in SECTION_HEADERS) and len(l.split()) <= 5:
            if buffer:
                sections.setdefault(current, "")
                sections[current] += "\n".join(buffer) + "\n"
                buffer = []
            current = low
            continue
        buffer.append(l)
    if buffer:
        sections.setdefault(current, "")
        sections[current] += "\n".join(buffer) + "\n"
    return sections

def extract_name(doc) -> str:
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            if ent.start_char < 120:
                return ent.text
    first_line = doc.text.strip().splitlines()[0]
    if len(first_line.split()) <= 4:
        return first_line.strip()
    return "Candidate"

def parse_experience_block(block_text: str) -> List[Dict[str, Any]]:
    out = []
    lines = [l.strip() for l in block_text.splitlines() if l.strip()]
    # Simplified parsing for robustness
    for line in lines:
        if DATE_RANGE_RE.search(line):
             out.append({"title": line, "date_text": DATE_RANGE_RE.search(line).group(0), "bullets": []})
    return out

def parse_text(text: str) -> Dict[str, Any]:
    doc = nlp(text)
    return {
        "name": extract_name(doc),
        "emails": extract_emails(text),
        "phones": extract_phones(text),
        "skills": extract_skills(text),
        "sections": list(split_into_sections(text).keys()),
        "raw_text": text
    }