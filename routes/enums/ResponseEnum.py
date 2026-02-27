from enum import Enum

class ResponseSignal(Enum):

    DOWNLOAD_FILES_FAILURE = "failed_to_download_files"
    NO_DOWNLOADED_FILES = "no_downloaded_files_to_process"
    FILES_METADATA_EXTRACTION_FAILURE = "failed_to_extract_files_metadata"
    TEXT_EXTRACTION_SUCCESS = "text_extracted_successfully"
    CHUNKING_FAILURE = "failed_to_chunk_text"
    CHUNKING_SUCCEEDED = "text_chunked_successfully"
    VECTORDB_STORAGE_SUCCESS = "vectordb_stored_successfully"
    DATABASE_LOADING_FAILURE = "failed_to_load_database"
    RETRIEVAL_FAILURE = "failed_to_retrieve_relevant_documents"
    INVALID_K_NUMBER = "invalid_k_number"
