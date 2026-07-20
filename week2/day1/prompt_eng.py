import os
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel
import json

# -------------------------------
# Load API Key
# -------------------------------
load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("Check the API key")

client = Groq(api_key=my_api_key)
model = "llama-3.3-70b-versatile"

# -------------------------------
# Structured Output
# -------------------------------
class Category(BaseModel):
    category: str

schema = Category.model_json_schema()

response_format = {
    "type": "json_object"
}

# -------------------------------
# System Prompt
# -------------------------------
system_prompt = f"""
You are an AI Customer Support Assistant for a Laptop and Mobile Service Center.

Your task is to classify the customer's query into exactly one category.

Categories:

1. BILLING
- Payment issues
- Refunds
- Invoice
- Warranty charges
- Subscription charges

2. TECHNICAL
- Laptop problems
- Mobile problems
- Battery issues
- Screen issues
- Charging issues
- Software issues
- Hardware issues
- Internet issues

3. OTHER
- Greetings
- Feedback
- General questions
- Anything that is neither billing nor technical

Return ONLY valid JSON matching this schema:

{schema}

Rules:
- Choose only one category.
- Do not explain your answer.
- Return only JSON.
"""

system_message = {
    "role": "system",
    "content": system_prompt
}

query = input("Enter your query: ")

user_message = {
    "role": "user",
    "content": query
}

messages = [system_message, user_message]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=0,
    response_format=response_format
)

ans = response.choices[0].message.content

data = json.loads(ans)

result = Category(**data)

print("\nCategory :", result.category)