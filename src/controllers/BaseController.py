from config import get_settings, Settings
import os
import shutil
from pathlib import Path
from config.logging_config import get_logger
class BaseController:
    """
    Handles directories creation.
    """

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
        self.logger = get_logger(__name__)

      

  
    def get_txt_files_dir(self) -> Path:
        txt_dir = Path(self.txt_files_dir)

        try:
            txt_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            self.logger.error(f"Failed to create directory {txt_dir}: {e}")
            raise

        return txt_dir

    def get_pdf_files_dir(self):
        pdfs_dir = Path(self.pdf_files_dir)
        try:
            pdfs_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            self.logger.error(f"Failed to create directory {pdfs_dir}: {e}")

        return pdfs_dir
    
    def get_files_metadata_path(self):
        files_metadata_path = Path(self.metadata_path)
        try:
            files_metadata_path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            self.logger.error(f"Failed to create directory {files_metadata_path}: {e}")
        
        return files_metadata_path / "files_metadata.json"       
    
    def get_output_dir(self):
        output_dir = Path(self.output_dir)
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            self.logger.error(f"Failed to create directory {output_dir}: {e}")
        
        return output_dir  
    
    def get_db_dir(self):
        db_dir = Path(self.app_settings.DATABASE_DIR)

        try:
            if db_dir.exists():
                shutil.rmtree(db_dir)
                self.logger.info(f"Removed existing database directory: {db_dir}")

            db_dir.mkdir(parents=True, exist_ok=True)

        except OSError as e:
            self.logger.error(f"Failed to reset database directory {db_dir}: {e}")
        
        return db_dir
    