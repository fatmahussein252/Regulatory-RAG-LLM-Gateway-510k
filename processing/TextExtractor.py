import pdfplumber 
from config import Settings, get_settings
from controllers import BaseController
import os
import re
import json
from pathlib import Path

class TextExtractor:
    def __init__(self, base_controller: BaseController):
        self.app_settings = get_settings()
        self.base_controller = base_controller
        self.txt_files_dir = self.base_controller.get_txt_files_dir()
    
   

    def clean_text(self, text: str) -> str: 
        # Remove lines that contain only spaces/tabs 
        text = re.sub(r'^[ \t]+$', '', text, flags=re.MULTILINE) 
        # Replace multiple blank lines with a maximum of two 
        text = re.sub(r'\n{3,}', '\n\n', text) 
        # Strip trailing spaces on each line 
        text = re.sub(r'[ \t]+$', '', text, flags=re.MULTILINE) 
        # Remove excessive internal spacing (but keep single spaces) 
        text = re.sub(r'[ \t]{2,}', ' ', text) 
        
        return text.strip()
    
    def extract_text(self, file_path: str, file_source: str):
        with pdfplumber.open(file_path) as pdf:
            self.pdf_instance = pdf
        
            self.metadata = self.pdf_instance.metadata
            self.pages = self.pdf_instance.pages
            self.doc_k_number = Path(file_path).stem
            
            txt_file_path = os.path.join(self.txt_files_dir,f"{self.doc_k_number}.txt")
            if os.path.exists(txt_file_path):
                os.remove(txt_file_path)

            pages_list = []
            for page in self.pages:

                # Extract text
                page_text = page.extract_text(layout=True) or ""
                
                cleaned_page_text = self.clean_text(page_text)
                
                with open(txt_file_path, 'a') as f:
                    f.write(cleaned_page_text + '\n')

               
                pages_list.append(
                    {
                    "page_content": cleaned_page_text,
                    "metadata": {
                        "k_number": self.doc_k_number,
                        "source_url": file_source,
                        "page_number": page.page_number,
                        }
                    } 
                )

            return pages_list
         
            
         
        
        
