import os
import json
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel
from pypdf import PdfReader


# ==========================================
# Load Environment Variables
# ==========================================

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("Groq API Key Issue")

client = Groq(api_key=my_api_key)

model = "llama-3.3-70b-versatile"


# ==========================================
# Resume Path
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

RESUME_PATH = "/workspaces/AI_handson/week2/chatbot_backend/Resume/MugdhaTadwalkar_CV.pdf"


# ==========================================
# Read Resume
# ==========================================

def read_resume():

    reader = PdfReader(RESUME_PATH)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


resume_text = read_resume()


# ==========================================
# Pydantic Models
# ==========================================

class Experience(BaseModel):
    company: str
    role: str
    duration: str
    description: str


class Resume(BaseModel):
    name: str
    phone: str
    email: str
    github: str
    linkedin: str
    location: str
    summary: str
    experience: list[Experience]
    projects: list[str]
    skills: list[str]
    certifications: list[str]


# ==========================================
# Resume Parsing
# ==========================================

Resume_schema = Resume.model_json_schema()


system_prompt = f"""
You are an expert resume parser.

Extract structured information from the resume.

Return ONLY valid JSON following this schema.

Schema:
{Resume_schema}

Rules:

1. Follow the schema exactly.
2. Do not add extra fields.
3. Do not guess.
4. Missing string -> ""
5. Missing list -> []
6. Return ONLY JSON.
"""


user_prompt = f"""
Extract the structured information from this resume.

Resume:

{resume_text}
"""


response = client.chat.completions.create(

    model=model,

    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ],

    temperature=0,

    response_format={
        "type": "json_object"
    }
)


# ==========================================
# Convert LLM Response to Resume Object
# ==========================================

resume_data = json.loads(
    response.choices[0].message.content
)

resume = Resume(**resume_data)

resume_json = resume.model_dump_json(indent=2)


# ==========================================
# Chatbot System Prompt
# ==========================================

chatbot_system_prompt = f"""
You are a helpful AI Resume Assistant.

You have access to the following resume:

{resume_json}

Your job is to answer questions about the candidate.

Rules:

1. Answer ONLY using information from the resume.
2. Never make up information.
3. If the answer is not available in the resume, say:

"This information is not available in the resume."

4. Answer naturally in plain English.
5. Do NOT return JSON unless the user explicitly asks for JSON.
6. Keep answers concise and conversational.
"""


# ==========================================
# Chat Function
# ==========================================

def answer_question(question: str):

    chat_messages = [
        {
            "role": "system",
            "content": chatbot_system_prompt
        },
        {
            "role": "user",
            "content": question
        }
    ]

    response = client.chat.completions.create(

        model=model,

        messages=chat_messages,

        temperature=0
    )

    answer = response.choices[0].message.content

    return answer

#query="projects"
#result=answer_question(query)
#print(result)