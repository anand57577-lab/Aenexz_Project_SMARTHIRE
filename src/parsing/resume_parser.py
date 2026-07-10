import os
import fitz                    
from docx import Document


class ResumeParser:

    def __init__(self):

        self.allowed_extensions = [
            ".pdf",
            ".docx"
        ]
 
    # Validate File 

    def validate_file(self, file_path):

        extension = os.path.splitext(file_path)[1].lower()

        if extension not in self.allowed_extensions:

            raise ValueError(
                f"Unsupported file type : {extension}"
            )

        return extension
 
    # PDF Parser 
    
    def parse_pdf(self, file_path):
        try:
            document = fitz.open(file_path)

            text = ""

            for page in document:
                text += page.get_text()

            document.close()

            return text.strip()

        except Exception as e:
            raise Exception(f"Error parsing PDF: {e}")
 
    # DOCX Parser 

    def parse_docx(self, file_path):
        try:
            document = Document(file_path)

            text = []

            for paragraph in document.paragraphs:

                text.append(paragraph.text)

            return "\n".join(text).strip()
    
        except Exception as e:
            raise Exception(f"Error parsing PDF: {e}")
        

    def parse(self, file_path):

        extension = self.validate_file(file_path)

        if extension == ".pdf":

            return self.parse_pdf(file_path)

        elif extension == ".docx":

            return self.parse_docx(file_path)

        else:

            raise ValueError(
                "Unsupported Resume Format"
            )