from config import Settings, get_settings, get_pdfs_urls
from controllers import BaseController
import requests
from urllib.parse import urlparse
import os
from datetime import datetime
import json
from pathlib import Path
import logging

class Downloader:
    def __init__(self, base_controller: BaseController):
        self.app_settings = get_settings()
        self.base_controller = base_controller
        self.pdf_files_dir = self.base_controller.get_pdf_files_dir()
        self.metadata_path = self.base_controller.get_files_metadata_path()
        self.files_sources = get_pdfs_urls()
        self.logger = logging.getLogger(__file__)

    def download_and_save_files(self):
        for file_source in self.files_sources:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(file_source, headers=headers, stream=True)
            response.raise_for_status()

            if "application/pdf" not in response.headers.get("Content-Type", ""):
                raise ValueError("URL did not return a PDF")
          
            parsed_url = urlparse(file_source)
            filename = os.path.basename(parsed_url.path)

            if not os.path.exists(self.pdf_files_dir):
                os.makedirs(self.pdf_files_dir)
            
            file_path = os.path.join(
                self.pdf_files_dir,
                filename
            )

            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        downloaded_files = len(os.listdir(self.pdf_files_dir))
        return downloaded_files
    
    def save_files_metadata(self):
        metadata = {}

        for file in self.files_sources:
            parsed_url = urlparse(file)
            filename = os.path.basename(parsed_url.path)
            metadata[filename]= {
                        "doc_id": Path(filename).stem,
                        "URL": file,
                        "retrieved_at": datetime.utcnow().isoformat() + "Z"
                    }
            
        try:
            with open(self.metadata_path, "w") as f:
                json.dump(metadata, f, indent=4)

            
            # Read and return content
            with open(self.metadata_path, "r") as f:
                content = json.load(f)

            return content

        except Exception as e:
            self.logger.error(f"Error writing metadata file: {e}")
            return None