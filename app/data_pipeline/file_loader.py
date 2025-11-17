import docx2txt
import PyPDF2
import os

class FileLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        ext = os.path.splitext(self.file_path)[-1].lower()

        if ext == ".pdf":
            return self._load_pdf()
        elif ext == ".docx":
            return self._load_docx()
        else:
            raise ValueError("Unsupported file format")

    def _load_pdf(self):
        text = ""
        with open(self.file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text

    def _load_docx(self):
        return docx2txt.process(self.file_path)
