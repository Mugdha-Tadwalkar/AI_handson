import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv
import json
from pypdf import PdfReader


load_dotenv()

my_api_key=os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("Check the api key")

client=Groq(api_key=my_api_key)
model="llama-3.3-70b-versatile"

from pydantic import BaseModel

def read_pdf():
    text = ""

    reader = PdfReader("/workspaces/AI_handson/week2/resume_chatbot/Resume/MugdhaTadwalkar_CV.pdf")

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text

class Experience(BaseModel):
    company:str
    role:str
    description:str
    duration:str

class Resume(BaseModel):
    name:str
    education:list[str]
    cgpa:float
    skills:list[str] 
    projects:list[str]    
    certifications:list[str]
    linkedin:str
    github:str
    contactno:str
    experience:list[Experience]


schema=Resume.model_json_schema()

response_format={
    "type":"json_object"
}

resume_system_prompt = f"""
You are an expert resume parser.

Your task is to extract structured information from the given resume and return it as valid JSON.

The resume may contain information in different formats and section names. Extract information based on its meaning, not just the section headings.

Examples:
- "Experience", "Professional Experience", "Employment", "Work History", and "Internships" all represent work experience.
- Skills may appear in dedicated skills sections, project descriptions, certifications, or work experience.
- Projects may appear under "Projects", "Academic Projects", "Personal Projects", or within experience.

Return ONLY a valid JSON object that strictly follows the schema below.

JSON Schema:
{schema}

Rules:
1. Follow the JSON schema exactly.
2. Do NOT add fields that are not present in the schema.
3. Extract only information explicitly mentioned in the resume.
4. Do NOT guess, infer, or fabricate any information.
5. If a string field is missing, return an empty string ("").
6. If a list field has no information, return an empty list ([]).
7. Preserve the original wording as much as possible.
8. Remove duplicate values from lists while preserving order.
9. Return ONLY the JSON object. Do not include explanations, markdown, or code fences.
"""


resume_system_message={
    "role":"system",
    "content":resume_system_prompt
}


resume_text=read_pdf()

user_prompt = f"""
Extract the structured information from the following resume.

Resume:

{resume_text}
"""

resume_user_message={
    "role":"user",
    "content":user_prompt

}
messages=[resume_system_message,resume_user_message]
response=client.chat.completions.create(model=model,messages=messages,temperature=0,response_format=response_format)
ans=response.choices[0].message.content
print(ans)
