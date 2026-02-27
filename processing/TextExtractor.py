import pdfplumber 
from config import Settings, get_settings
from controllers import BaseController
import os
import re
import json
from pathlib import Path
from config.logging_config import get_logger

class TextExtractor:
    """
    Extracts and clean text from PDFs.
    Stores text files.
    """
    def __init__(self, base_controller: BaseController):
        self.app_settings = get_settings()
        self.base_controller = base_controller
        self.txt_files_dir = self.base_controller.get_txt_files_dir()
        self.logger = get_logger(__name__)
    
   
    def save_text(self, cleaned_page_text):
        """
        Save cleaned text.
        """
         
        try: 
            with open(self.txt_file_path, 'a') as f:
                        f.write(cleaned_page_text + '\n')
        except Exception as e:
            self.logger.error(f"Error writing txt file: {e}")
        
            
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
        """
        Extract text from pdf files.
        Returns:
            List[dict]: List of dictionary contains pages text and metadata.
        """
        with pdfplumber.open(file_path) as pdf:
            self.pdf_instance = pdf
        
            self.metadata = self.pdf_instance.metadata
            self.pages = self.pdf_instance.pages
            self.doc_k_number = Path(file_path).stem
            
            self.txt_file_path = os.path.join(self.txt_files_dir,f"{self.doc_k_number}.txt")
            
            if os.path.exists(self.txt_file_path):
                os.remove(self.txt_file_path)

            pages_list = []
            for page in self.pages:

                # Extract text
                page_text = page.extract_text(layout=True) or ""
                
                cleaned_page_text = self.clean_text(page_text)
                
                self.save_text(cleaned_page_text=cleaned_page_text)

               
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
        

         
            
         
        
        
