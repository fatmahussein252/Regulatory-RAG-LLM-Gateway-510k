# System Architecture

The system follows this pipeline:

1. Ingestion → Download FDA 510(k) PDFs
2. Processing → Extract and clean text
3. Chunking → Split text into overlapping chunks
4. Embedding → Generate vector embeddings
5. Retrieval → Filter by k_number and retrieve relevant chunks
6. LLM Gateway → Extract structured regulatory data
7. Output → Store grounded JSON results

## System Components

### Ingestion Module
Handles downloading FDA 510(k) PDF documents and extracting files metadata (doc_id, URL, retrieved_at).

### Document Processing Module
Transforms raw PDF files into clean text pages list with metadata (k_number, source_url, page_number).

**Responsibilities:** 
- Extract text from PDFs
- Normalize whitespace
- Remove excessive blank lines
- Generates list of pages text with metadata

### Chunking Module
Applies a page-aware recursive character chunking strategy using `RecursiveCharacterTextSplitter`.

**Responsibilities:**
- Each PDF page is first converted into a LangChain Document object containing:
    - page_content: Extracted text from the page
    - metadata: Associated metadata (e.g., k_number, page_number)

- The page documents are split into smaller overlapping chunks using a configurable:
    - chunk_size (default: 1200 characters)
    - chunk_overlap (default: 400 characters)


### Embedding & Vector Store Module

Converts text chunks into embeddings and stores them in a persistent vector database.

**Responsibilities:**
- Generate embeddings using configured embedding model
- Store embeddings in vector store (e.g., ChromaDB)
- Persist index under `vectorDB/`


### Retrieval Module
Uses semantic similarity search with optional metadata filtering to retrieve relevant document chunks from a persistent Chroma vector store.

**Responsibilities:**
- Loads a persisted ChromaDB instance using the configured embedding function.
- For each user query:
    - The query is converted into an embedding using the same embedding model used during indexing.
    - A configurable top-k (default = 5) similarity search is performed to retrieve the most relevant chunks with optional metadata filtering.
    - Returns The matched Document chunks, their associated distance scores and preserved metadata.

### LLM Gateway (OpenRouter provider)
Abstracts interaction with external large language models via OpenRouter. It encapsulates model initialization, prompt construction, and structured output enforcement.

**Responsibilities:**
- Initialize the configured LLM model via OpenRouter.
- **Model Configuration:**
    - Configurable model_name (default model: stepfun/step-3.5-flash:free)
    - Low temperature (0.2) for deterministic outputs
    - Timeout and retry handling
    - API Key loaded from environment settings
- Construct a strict system prompt for grounded extraction.
- **Prompt Design:**
The system prompt enforces:
    - JSON-only output
    - No explanations or markdown
    - No inference beyond provided context
    - Explicit null handling for missing fields
    - Mandatory citation grounding using chunk_id and exact snippets
- Enforce structured JSON output using langchain `JsonOutputParser`.
- Return a chain of prompt template, llm and output parser to invoke.












