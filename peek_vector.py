# Checking that how the vectors present in our db looks like 

import chromadb

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("govt_schemes")

result = collection.get(ids=["chunk_0"], include=["embeddings", "documents", "metadatas"])

print("Text of this chunk:")
print(result["documents"][0][:200], "\n")

print("Metadata:")
print(result["metadatas"][0], "\n")

print("Vector length:", len(result["embeddings"][0]))
print("First 5 numbers of the vector:")
print(result["embeddings"][0][:5])