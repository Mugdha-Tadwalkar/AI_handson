#helps python interact with your computer
import os

#Makes it easy to work with files and folders
from pathlib import Path

#This reads your .env file so that your API keys are available in python
from dotenv import load_dotenv

#Lets your python program send request to Groq AI models
from groq import Groq

# Loads the values from the .env file into your program
load_dotenv()

# Gets the value of GROQ_API_KEY from the environment variables
my_api_key=os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("Check the API key")

client = Groq(api_key=my_api_key)
model= "llama-3.3-70b-versatile"

role="user"
prompt="i love my india"
message={
    "role":role,
    "content":prompt
}
messages=[message]
response=client.chat.completions.create(model=model,messages=messages)

answer=response.choices[0].message.content
print(answer)


