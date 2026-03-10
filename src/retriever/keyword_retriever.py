from langchain_community.retrievers import BM25Retriever
from config.logging_config import get_logger

class BMRetriever:
    def __init__(self):
        self.k_numbers = ["K221000", "K232639", "K230909"]
        self.logger = get_logger(__name__)

    def retrieve_docs(self, keyword_index: BM25Retriever, query: str, metadata_filter: str):
        if metadata_filter not in self.k_numbers:
            self.logger.error("\n Invalid metadata filter.\n")
            return None
        filtered_docs = []
        relevant_docs = keyword_index.invoke(input=query)
        for doc in relevant_docs:
            if doc.metadata["k_number"] == metadata_filter:
                filtered_docs.append(doc)

        return filtered_docs

        
