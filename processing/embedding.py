from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma.vectorstores import Chroma

from config import Settings, get_settings
import logging
class Embedding:
    """
    Store vectordatabase using chromadb
    """
    def __init__(self):
        self.settings = get_settings()
        self.embedding_model_name = self.settings.EMBEDDING_MODEL
        self.logger = logging.getLogger(__name__)
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model_name,
            model_kwargs={"device": "cpu"}
        )

    
    def embed_text(self, chunks, persist_directory):
        """        
        Store vectore database.
        Returns:
            vectorstore object: chromadb vectorstore object.
        """
        self.logger.info(f"storing vectorDB at {persist_directory}...")
        # Store in Chroma
        return Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=persist_directory
        )

    