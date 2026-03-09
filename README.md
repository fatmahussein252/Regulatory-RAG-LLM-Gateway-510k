# FDA 510(k) Regulatory RAG & LLM Gateway
A mini end-to-end system that ingests FDA 510(k) documents, builds a RAG index, and uses an LLM Gateway to extract regulatory facts into a structured JSON output grounded by citations.

## Requirements

- Python 3.13 (Python 3.14 causes compatibility issues with ChromaDB) 

#### Install Python using MiniConda

1) Download and install MiniConda from [here](https://docs.anaconda.com/free/miniconda/#quick-command-line-install)
2) Create a new environment using the following command:
```bash
$ conda create -n regulatory-rag python=3.13
```
3) Activate the environment:
```bash
$ conda activate regulatory-rag
```


## Installation
### Clone the project
```bash
$ git clone git@github.com:fatmahussein252/Regulatory-RAG-LLM-Gateway-510k.git
$ cd Regulatory-RAG-LLM-Gateway-510k/src
```
### Install the required packages

```bash
$ pip install -r ../requirements.txt
```

### Setup the environment variables

```bash
$ cp .env.example .env
```
1) Get an OpenRouter API key from [here](https://openrouter.ai/)
2) Set your `OPENROUTER_API_KEY` environment variable value in the `.env` file.

## Run the FastAPI Server
```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```
Go to the FastAPI-Swagger UI [here](http://0.0.0.0:5000/docs)


## Ingestion
`ingest` endpoint: 
- Downloads pdf files and stores them at Assets/k_pdf_files directory.
- Extracts files metadata and stores at Assets/files_metadata.json
- Returns metadata of the downloaded files.

## Documents Processing
`process_docs` endpoint:
- Extracts text from PDFs 
- Cleans text (e.g. removes multiple blank lines and excessive internal spacing)
- Stores text files at Assets/k_txt_files

## Chunking, Embedding and Vectorstore
`embed_docs` endpoint:
- Chunks text pages with metadata 
- Generates embeddings and stores them in a persistent vector database under the vectorDB/    directory.

Schema: 
```json
{
  "chunk_size": 0, # defaults to 1200
  "chunk_overlap_size": 0 # defaults to 400
}
```

## Retrieval
`retrieve` endpoint retrieves the top_k relevant documents to the query using k_number filter.

Schema: 
```json
{
  "query": "string",  
  "k_number": "string", 
  "top_k": 5
}
```
## LLM Gateway
`llm_gateway` enpoint:
- Retrieves relevant documents 
- Sends query and context to the llm for output extraction.
- Returns extracted output

Schema: 
```json
{
  "query": "string",
  "model_name": "string", # defaults to "stepfun/step-3.5-flash:free"
  "k_number": "string"
}
```
 ## Extraction
`extract` endpoint:
- Generates a structured, citation-grounded JSON output saved at: Output/extraction_<k_number>.json
- Returns extracted JSON output.

Schema: 
```json
{
  "k_number": "string",
  "model_name": "string"  # defaults to "stepfun/step-3.5-flash:free"
}
```
## Output Example
Find examples under src/output_example









