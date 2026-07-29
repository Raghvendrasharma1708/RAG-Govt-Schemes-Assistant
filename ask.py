import os 
from dotenv import load_dotenv
from openai import OpenAI
import chromadb

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("govt_schemes")

def retrieve_answer(question ,n_results=8):
    response = client.embeddings.create(
        model = 'text-embedding-3-small',
        input= [question]
    )

    question_embedding = response.data[0].embedding

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
    )

    chunks= []
    for i , doc in enumerate(results["documents"][0]):
        meta = results["metadatas"][0][i]
        chunks.append(f'[Source: {meta["source"]}, Page: {meta["page"]}]\n {doc}')

    return chunks

def build_prompt(question,chunks):
    context = "\n\n---\n\n".join(chunks)
    return f"""You are an assistant that answers questions about Indian government schemes and policies.

RULES:
1. Answer ONLY using the context provided below. Do not use any outside knowledge.
2. Every claim in your answer must cite its source in the format (Source: document_name, Page: X).
3. If the context does not contain the answer, say exactly: "I could not find this information in the available documents." Do not guess.
4. Keep answers clear and simple, understandable by a common citizen.

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""

def ask(question):
    chunks = retrieve_answer(question)
    
    prompt = build_prompt(question, chunks)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print("Govt Schemes Q&A — type 'exit' to quit\n")
    while True:
        question = input("Your question: ")
        if question.strip().lower() == "exit":
            break
        print("\n" + ask(question) + "\n")   
  

    
            