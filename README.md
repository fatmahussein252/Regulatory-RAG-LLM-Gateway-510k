# Regulatory-RAG-LLM-Gateway-510-k-
A mini end-to-end system that ingests FDA 510(k) documents, builds a RAG index, and uses an LLM Gateway to extract regulatory facts into a structured JSON output grounded by citations.

## Requirements

- Python 3.13 (python 3.14 cuases compatibility issue with chromadb) 

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
$ git clone git@github.com:fatmahussein252/Regulatory-RAG-LLM-Gateway-510-k-.git
$ cd Regulatory-RAG-LLM-Gateway-510-k-/
```
### Install the required packages

```bash
$ pip install -r requirements.txt
```

### Setup the environment variables

```bash
$ cp .env.example .env
```
1) Get an OpenRouter API from [here] (https://openrouter.ai/)
2) Set your environment variables in the `.env` file. Like `OPENROUTER_API_KEY` value.

## Run the FastAPI Server
```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```
Go to the FastAPI-Swagger UI [here](http://0.0.0.0:5000/docs)


## Ingestion
`ingest` endpoint: 
- Download pdf files and store them at Assets/k_pdf_files directory.
- Extract files metadata and store at Assets/files_metadata.json
- Response with dowloaded files metadata.

## Documents Processing
`process_docs` enpoint:
- Extracts text from PDFs 
- Clean text (e.g. remove multiple blank lines and excessive internal spacing)
- Store text files at Assets/k_txt_files

## Chunking, Embedding and Vectorstore
`embed_docs` enpoint:
- Chunk text pages with metadata 
- Generate embeddings vectorstore at vectorDB directory

Schema: 
```json
{
  "chunk_size": 0, # defaults to 1200
  "chunk_overlap_size": 0 # defaults to 400
}
```

## Retrieval
`retrieve` enpoint retrieves the top_k relevant documents to the query using k_number filter.

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
- Retrieve relevant documents 
- Send query and context to the llm for output extraction.

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
- Generate the json output files at Output/extraction_<k_number>.json.
- Response with output path and extracted schema.

Schema: 
```json
{
  "k_number": "string",
  "model_name": "string"  # defaults to "stepfun/step-3.5-flash:free"
}
```







