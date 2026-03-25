from config import get_settings
from controllers import BaseController
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import HierarchicalNodeParser
from langchain_core.documents import Document
from config.logging_config import get_logger

class LlamaIndexChunker:
    def __init__(self):
        self.app_settings = get_settings()
        self.base_controller = BaseController()
        self.pdf_files_path = self.base_controller.get_pdf_files_dir()
        self.logger = get_logger(__name__)
        
    def get_llama_index_chunks(self):
        # Load PDF
        documents = SimpleDirectoryReader(input_dir=self.pdf_files_path).load_data()

        if not documents or len(documents) == 0:
            self.logger.error("SimpleDirectoryReader Failed to load PDFs")
        
        # Chunk (section-aware)
        parser = HierarchicalNodeParser.from_defaults(chunk_sizes=[1000], chunk_overlap=400)
        nodes = parser.get_nodes_from_documents(documents)

        if not nodes or len(nodes) == 0:
            self.logger.error("HierarchicalNodeParser Failed to chunk")

        # Get chunks as LangChain documents
        lc_docs = []

        for node in nodes:
            lc_docs.append(
                Document(
                    page_content=node.text,
                    metadata=node.metadata
                )
            )

        if not lc_docs or len(lc_docs) == 0:
            self.logger.error("Failed to get langchain documents")

        return lc_docs