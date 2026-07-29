# Indian Govt Schemes Assistant

A RAG-based Q&A system for Indian government scheme documents (PM-KISAN, Mudra Yojana, PMAY, FCRA, PMKVY, and more). Ask a question in plain language and get an answer with the exact source document and page number cited.

## How it works
1. PDFs are extracted and chunked (`extract_and_chunk.py`)
2. Chunks are embedded with OpenAI and stored in ChromaDB (`build_vectorstore.py`)
3. Questions are embedded and matched against stored chunks (retrieval)
4. Retrieved chunks are passed to gpt-4o-mini with a prompt that enforces citations and blocks hallucination (`ask.py`)
5. Streamlit provides the interface (`app.py`)

## Stack
Python, pypdf, OpenAI embeddings + gpt-4o-mini, ChromaDB, Streamlit

## Run locally
\`\`\`
pip install -r requirements.txt
streamlit run app.py
\`\`\`
Requires an `OPENAI_API_KEY` in a `.env` file.