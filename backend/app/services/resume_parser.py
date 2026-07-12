from pathlib import Path
import pdfplumber
from docx import Document


class ResumeParser:

    @staticmethod
    def extract_text(file_path: str):

        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":
            return ResumeParser.extract_pdf(file_path)

        elif extension == ".docx":
            return ResumeParser.extract_docx(file_path)

        else:
            raise ValueError("Unsupported file type")

    @staticmethod
    def extract_pdf(file_path):

        text = ""

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text

    @staticmethod
    def extract_docx(file_path):

        doc = Document(file_path)

        return "\n".join([paragraph.text for paragraph in doc.paragraphs])