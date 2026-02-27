from langchain_chroma.vectorstores import Chroma
from processing import Embedding
from config import get_settings


class Retriever:
    """
    Load vectorstore from persist directory.
    Retrieve related chunks using similarity search.
    """
    def __init__(self, persist_directory):
        self.persist_directory = persist_directory


    def load_vector_store(self, embedding: Embedding):
        """
        Loads vector database.
        Returns:
            vectorestore object: chromadb vectorstore
        """
        vectorstore = Chroma(persist_directory=self.persist_directory, embedding_function=embedding.embeddings)
        return vectorstore
    


    def retrieve_chunks(self, vectorstore, query, metadata_filter=None, k=5):
        """
        Retrieve relevant chunks from the vector store based on a query, with optional metadata filtering.
        Returns:
            List[Document]: List of retrieved chunks with metadata.
        """
        # Retrieve chunks with optional metadata filter

        search_kwargs = {"k": k}
        if metadata_filter:
            search_kwargs["filter"] = metadata_filter

        retrieved_docs_and_scores  = vectorstore.similarity_search_with_score(
            query=query,
            **search_kwargs
        )

        return retrieved_docs_and_scores

    