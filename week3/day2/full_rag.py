import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import numpy as np
from sentence_transformers import SentenceTransformer
import sys

load_dotenv()

myapikey=os.getenv("GROQ_API_KEY")


if not myapikey:
    raise ValueError("Check the API key")

client=Groq(api_key=myapikey)
groqmodel="llama-3.3-70b-versatile"
embedding_model=SentenceTransformer("all-MiniLM-L6-v2")#This is an embedding model that is required to create embeddings.

doc=[ "Employees receive 24 days of paid leave per year.",
   
    "Employees work from the office on Tuesday, Wednesday and Thursday. "
    "Monday and Friday are optional work-from-home days.",
   
    "Employees receive Rs 3000 per month for gym reimbursement.",
   
    "Employees can claim Rs 2000 per month for home internet.",
   
    "Employees have a 90 day notice period."
    ]

doc_embedding=embedding_model.encode(doc)#We have feed the data to embedding model and that data is being stored in this variable as embeddings.
def cosine_similarity(a, b):
    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )

def retrieve(qembed):
    scores=[]
    for i, embedding  in enumerate(doc_embedding):
        score=cosine_similarity(embedding ,qembed)
        scores.append((score,doc[i]))
    scores.sort(reverse=True)
    return scores[0]


def ask_llm(question,context):
    sys_prompt=f"""answer in one line only. Answer only based on this context. do not hallucinate. Context: {context}"""
    sys_message={
        "role":"system",
        "content":sys_prompt
    }
    user_message={
        "role":"user",
        "content":question
    }
    messages=[sys_message, user_message]
    response=client.chat.completions.create(model=groqmodel, messages=messages)
    answer=response.choices[0].message.content
    return answer


query = "how many days of holidays we will get?"
qembedding=embedding_model.encode(query)
score,context=retrieve(qembedding)
answer=ask_llm(query,context)
print(answer)


#print(sys.getsizeof(doc_embedding))

