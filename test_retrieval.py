import os
from dotenv import load_dotenv
from openai import OpenAI
import chromadb

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("govt_schemes")

question = "What documents are needed for FCRA registration?"

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=[question]
)
question_embedding = response.data[0].embedding

results = collection.query(
    query_embeddings=[question_embedding],
    n_results=3
)

for i, doc in enumerate(results["documents"][0]):
    meta = results["metadatas"][0][i]
    print(f"\n--- Result {i+1} (source: {meta['source']}, page: {meta['page']}) ---")
    print(doc[:300])