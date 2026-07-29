import json
import os
from dotenv import load_dotenv
from openai import OpenAI   
import chromadb


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Initialize the OpenAI client with the API key from the environment variable

chroma_client = chromadb.PersistentClient(path="./chroma_db")  # Initialize the ChromaDB client with a persistent storage path
collection = chroma_client.get_or_create_collection("govt_schemes")  # Get or create a collection named "govt_schemes" in the ChromaDB

with open('chunks.json','r',encoding='utf-8') as f:
    chunks = json.load(f)  # Load the chunks from the JSON file


batch_size = 50
for i in range(0, len(chunks),batch_size):
    batch= chunks[i:i + batch_size]  # Process the chunks in batches of 50
    texts= [c['text'] for c in batch]  # Extract the text from each chunk in the batch

    response = client.embeddings.create(
        model= "text-embedding-3-small",  # Use the "text-embedding-3-small" model for generating embeddings
        input= texts  # Provide the extracted texts as input to the embedding model
    )

    embeddings = [item.embedding for item in response.data]  # Extract the embeddings from the response

    ids = [f"chunk_{i+j}" for j in range(len(batch))]
    metadatas = [{"source": c["source"], "page": c["page"]} for c in batch]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas
    )
    print(f"Embedded and stored chunks {i} to {i+len(batch)-1}")

print("\nDone! Vector store built at ./chroma_db")
