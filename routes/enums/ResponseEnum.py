from enum import Enum

class ResponseSignal(Enum):

    DOWNLOAD_FILES_FAILURE = "failed_to_download_files"
    FILES_METADATA_EXTRACTION_FAILURE = "failed_to_extract_files_metadata"
    TEXT_EXTRACTION_SUCCESS = "text_extracted_successfully"
    CHUNKING_FAILURE = "failed_to_chunk_text"
    CHUNKING_SUCCEEDED = "text_chunked_successfully"
    VECTORDB_STORAGE_SUCCESS = "vectordb_stored_successfully"
    RETRIEVAL_FAILURE = "failed_to_retrieve_relevant_documents"
    INVALID_K_NUMBER = "invalid_k_number"
