from config import get_settings, Settings
import os
class BaseController:
    
    def __init__(self):

        self.app_settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.pdf_files_dir = os.path.join(
            self.base_dir,
            "Assets/k_pdf_files"
            )
        self.txt_files_dir = os.path.join(
            self.base_dir,
            "Assets/k_txt_files"
            )
        self.metadata_path = os.path.join(
            self.base_dir,
            "Assets"
            )
        self.output_dir = os.path.join(
            self.base_dir,
            "Output"
            )

      

    def get_txt_files_dir(self):
        if not os.path.exists(self.txt_files_dir):
            os.makedirs(self.txt_files_dir)
        
        return self.txt_files_dir
    
    def get_pdf_files_dir(self):
        if not os.path.exists(self.pdf_files_dir):
            os.makedirs(self.pdf_files_dir)
        
        return self.pdf_files_dir
    
    def get_files_metadata_path(self):
        if not os.path.exists(self.metadata_path):
            os.makedirs(self.metadata_path)
        
        return os.path.join(self.metadata_path, "files_metadata.json")
    
    def get_output_dir(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        return self.output_dir  
    