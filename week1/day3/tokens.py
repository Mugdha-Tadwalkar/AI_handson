import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

my_api_key=os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("Check the api key")

client=Groq(api_key=my_api_key)
model="llama-3.3-70b-versatile"
role="user"
prompt=input("Enter your query: ")
message_system={
    "role":"system",
    "content":"You are a technical support assistant who solves technical queries."
}

message={
    "role":role,
    "content":prompt
}
messages=[message_system,message]
response=client.chat.completions.create(model=model,messages=messages,temperature=0,max_tokens=200)
ans=response.choices[0].message.content
usage=response.usage
print(f"user query: {prompt} token consumption{usage.prompt_tokens} finish_reason{response.choices[0].finish_reason}")
print(f"AI answer: {ans} token consumption{usage.completion_tokens} finish_reason{response.choices[0].finish_reason}")
print(f"Total token consumption: {usage.total_tokens} finish_reason{response.choices[0].finish_reason} ")


