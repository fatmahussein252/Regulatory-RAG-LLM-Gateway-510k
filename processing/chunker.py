from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .chunk_enum import ChunkEnum

class Chunker:
    """
    Create page documents with metadata.
    Chunk documents.
    
    """
    def __init__(self):
        pass
        
    def create_page_documents(self, pages_list: list):
        """
        Create LangChain Document objects for each page of a book.
        Returns:
            List[Document]: List of Document objects with page content and metadata.
        """

        # Create Documents
        documents = [
            Document(
                page_content=page["page_content"],
                metadata=page["metadata"]
            )
            for page in pages_list
        ]

        return documents
    
    def chunk_documents(self, documents: list, chunk_size: int=None, chunk_overlap: int=None):
        """
        Split documents into smaller chunks for embedding.
        Returns:
            List[Document]: List of chunked Document objects with metadata.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap  
        )

        chunks = text_splitter.split_documents(documents)

        return chunks
