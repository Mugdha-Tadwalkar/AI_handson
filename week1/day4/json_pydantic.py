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
# structured output
from pydantic import BaseModel
class Ticket(BaseModel):
    name:str
    email:str
    issue:str
schema=Ticket.model_json_schema()
response_format={
    "type":"json_object"
}
system_prompt=f"""
Extract the personal information from the ticket strictly based on this schema and give a json output.
{schema}
"""

message_system={
    "role":"system",
    "content":system_prompt
}
text="I am Mugdha. My laptop is getting down frequently.Contact me at abc@gmail.com. I am sneezing. I catched cold."
prompt=f"""
This is customer ticket. Please extract the personal information from this data.
{text}
"""
message={
    "role":role,
    "content":prompt
}
messages=[message_system,message]
response=client.chat.completions.create(model=model,messages=messages,temperature=0,response_format=response_format)
ans=response.choices[0].message.content
#print(ans)
#how to make this output readable?
import json
raw_json=ans
data_file=json.loads(raw_json)
ticket=Ticket(**data_file)
print(ticket.name)
print(ticket.email)
print(ticket.issue)

