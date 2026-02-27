## System Architecture

The system follows this pipeline:

1. Ingestion → Download FDA 510(k) PDFs
2. Processing → Extract and clean text
3. Chunking → Split text into overlapping chunks
4. Embedding → Generate vector embeddings
5. Retrieval → Filter by k_number and retrieve relevant chunks
6. LLM Gateway → Extract structured regulatory data
7. Output → Store grounded JSON results

### Components
Major Subsystems

Ingestion Module

Downloads regulatory PDFs.

Metadata extraction and storage.

Processing Module

Normalizes and cleans text.

Preprocessing ensures consistent chunk ingestion.

VectorDB & Embedding Layer

Chunking strategy (overlap and size).

Embedding model choice and vector index type.

Retrieval Engine

How similarity search works.

Filtering by regulatory identifiers.

LLM Gateway

Interface with LLM via API gateway (OpenRouter or similar).

Logging and prompt shaping.

Extraction & Grounded Output

Schema generation.

Citation grounding for regulatory facts.