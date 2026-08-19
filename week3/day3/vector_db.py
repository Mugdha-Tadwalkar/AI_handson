#uv add python-dotenv groq numpy sentence-transformers qdrant-client

import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from groq import Groq
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

load_dotenv()
groq_apikey=os.getenv("GROQ_API_KEY")
qdrant_apikey=os.getenv("QDRANT_API_KEY")
qdrant_url=os.getenv("QDRANT_URL")

if not GROQ_API_KEY or QDRANT_API_KEY or QDRANT_URL:
    print("Check your GROQ or QDRANT api key or URL")

groq_client=Groq(api_key=groq_apikey)
db_client=Qdrant(api_key=qdrant_apikey, url=qdrant_url)

print("now we are connected to qdrant and groq")

#------------------Create a collection

collection_name="knowledge"
embedding_size=384

# Delete collection if it already exists
if db_client.collection_exists(collection_name):
    print(f"Deleting existing collection: {collection_name}")
    db_client.delete_collection(collection_name)

#Create collection
db_client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(
        size=embedding_size,
        distance=Distance.COSINE,
    ),
)
print(f"Created collection: {collection_name}")
print(f"Vector size: {embedding_size}")
print("Distance: COSINE")

with open("knowledge.txt", "r", encoding="utf-8") as f:
    documents = [
        line.strip()
        for line in f
        if line.strip()
    ]

print(f"Loaded {len(documents)} documents")

#----------------now we are creating embeddings

model = SentenceTransformer("all-MiniLM-L6-v2")
print("Embedding model ready!")
embeddings = model.encode(documents)

print(f"Generated {len(embeddings)} embeddings")
print(f"Embedding size: {len(embeddings[0])}")

#Creating Qdrant Points

points = []

for i, embedding in enumerate(embeddings):

    point = PointStruct(
        id=i + 1, #id=1

        vector=embedding.tolist(),

        payload={
            "text": documents[i]
        }
    )
    points.append(point)

    #Uploading on Qdrant
db_client.upsert( #upload+insert
    collection_name=collection_name,
    points=points
)

print(f"Uploaded {len(points)} documents to Qdrant!")

#Search Qdrant
def search(query, top_k=3):

    # Convert the question into an embedding
    query_vector = model.encode(query).tolist()

    # Search Qdrant for similar vectors
    results = db_client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k,
        with_payload=True,
    ).points

    return results

#Asking the LLM
def ask_llm(question, context):

    prompt = f"""
Answer the question using only the information provided below.

Context:
{context}

Question:
{question}

If the answer is not present in the context, say:
"I don't know based on the provided information."
"""

    response = llm_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
question = "How many vacation days do I get?"

results = search(question, top_k=3)


# Extract text from the search results
context = "\n".join(
    result.payload["text"]
    for result in results
)


answer = ask_llm(question, context)


print("\nFinal Answer:")
print(answer)

question = "How many vacation days do I get?"

results = search(question, top_k=3)


# Extract text from the search results
context = "\n".join(
    result.payload["text"]
    for result in results
)


answer = ask_llm(question, context)


print("\nFinal Answer:")
print(answer)