import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv
import json
from pypdf import PdfReader
from docx import Document

load_dotenv()

my_api_key=os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("Check the api key")

client=Groq(api_key=my_api_key)
model="llama-3.3-70b-versatile"

# structured output
from pydantic import BaseModel
class JD(BaseModel):
    job_role:str
    req_skills:list[str]
    pref_skills:list[str]
    min_experience:float | None
    education_req:list[str]
    responsibilities:list[str]
JD_schema=JD.model_json_schema()
response_format={
    "type":"json_object"
}

jd_system_prompt=f"""
You are an expert HR assistant.

Your job is to analyze job descriptions and extract
structured information from them.

Return ONLY valid JSON matching this schema:

{JD_schema}
IMPORTANT:
Do NOT return the schema itself.
Do NOT return fields like "properties", "title" or "type".
Fill the schema with actual information extracted from the job description.



If minimum experience is not mentioned, return null.
If information for a list is missing, return an empty list.
Do not invent information.
"""

jd_system_message={
    "role":"system",
    "content":jd_system_prompt
}

job_desc="""
Description
Do you want to solve real customer problems through innovative technology? Do you enjoy working on scalable services in a collaborative team environment? Do you want to see your code directly impact millions of customers worldwide?

At Amazon, we hire the best minds in technology to innovate and build on behalf of our customers. Customer obsession is part of our company DNA, which has made us one of the world's most beloved brands.

Our Software Development Engineers (SDEs) use modern technology to solve complex problems while seeing their work's impact first-hand. The challenges SDEs solve at Amazon are meaningful and influence millions of customers, sellers, and products globally. We seek individuals passionate about creating new products, features, and services while managing ambiguity in an environment where development cycles are measured in weeks, not years.

At Amazon, we believe in ownership at every level. As an SDE-I, you'll own the entire lifecycle of your code - from design through deployment and ongoing operations. This ownership mindset, combined with our commitment to operational excellence, ensures we deliver the highest quality solutions for our customers.

We're looking for curious minds who think big and want to define tomorrow's technology. At Amazon, you'll grow into the high-impact engineer you know you can be, supported by a culture of learning and mentorship. Every day brings exciting new challenges and opportunities for personal growth.
Key job responsibilities
• Collaborate and communicate effectively with experienced cross-disciplinary Amazonians to design, build, and operate innovative products and services that delight our customers, while participating in technical discussions to drive solutions forward.
• Design and develop scalable solutions using cloud-native architectures and microservices in a large distributed computing environment.
• Participate in code reviews and contribute to technical documentation.
• Build and maintain resilient distributed systems that are scalable, fault-tolerant, and cost-effective.
• Leverage and contribute to the development of GenAI and AI-powered tools to enhance development productivity while staying current with emerging technologies.
• Write clean, maintainable code following best practices and design patterns.
• Work in an agile environment practicing CI/CD principles while participating in operational responsibilities including on-call duties.
• Demonstrate operational excellence through monitoring, troubleshooting, and resolving production issues.
Basic Qualifications
- Experience with at least one general-purpose programming language such as Java, Python, C++, C#, Go, Rust, or TypeScript
- Experience with data structure implementation, basic algorithm development, and/or object-oriented design principles
- Currently has, or is in the process of obtaining a bachelor’s degree in Computer Science, Computer Engineering, Data Science, Information Systems, or related STEM fields
- Must be 18 years of age of older
Preferred Qualifications
- Experience from previous technical internship(s) or demonstrated project experience
- Experience with one or more of the following: AI tools for development productivity, Cloud platforms (preferably AWS), Database systems (SQL and NoSQL), Contributing to open-source projects, Version control systems, Debugging and troubleshooting complex systems
- Demonstrated ability to learn and adapt to new technologies quickly
- Basic understanding of software development lifecycle (SDLC)
- Strong problem-solving and analytical skills
- Excellent written and verbal communication skills
"""

user_prompt=f"""
Analyze the following Job Description
{job_desc}
"""

user_message={
    "role":"user",
    "content":user_prompt
}

messages=[jd_system_message,user_message]
response=client.chat.completions.create(model=model,messages=messages,temperature=0,response_format=response_format)
ans=response.choices[0].message.content
raw_json=ans
data_file=json.loads(raw_json)
jd=JD(**data_file)
#print("Education Required : ",jd.education_req)
#print("Role : ",jd.job_role)

resume_folder = Path("Resume")

# print("\nFiles present in Resume folder:\n")

#iterdir means it will give everything inside the folder.
# for file in resume_folder.iterdir():
#     if file.is_file():
#         print(file.name)

# Function to extract text from PDF
def read_pdf(file_path):
    text = ""

    reader = PdfReader(file_path)

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# Function to extract text from DOCX
def read_docx(file_path):
    text = ""

    doc = Document(file_path)

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text

#structuring Resume object

class Resume(BaseModel):
    name: str
    email: str
    skills: list[str]
    experience: float | None
    education: list[str]
    projects: list[str]

Resume_schema=Resume.model_json_schema()

response_format={
    "type":"json_object"
}

resume_system_prompt = f"""
You are an expert HR assistant.

Your job is to analyze resumes and extract
structured information from them.

Return ONLY valid JSON matching this schema:

{Resume_schema}

IMPORTANT:
Do NOT return the schema itself.
Do NOT return fields like "properties", "title" or "type".
Fill the schema with actual information extracted from the resume.

Rules:
- Extract the candidate's full name.
- Extract the email address. If not available, return an empty string.
- Extract all technical skills as a list.
- Extract the total years of professional experience. If not mentioned, return null.
- Extract all educational qualifications as a list.
- Extract major projects as a list.
- Do not invent information.
- If any list field is missing, return an empty list.
- Return ONLY valid JSON.
"""
resume_system_message={
    "role":"system",
    "content":resume_system_prompt
}

# -------------------------------
# Read and Structure Every Resume
# -------------------------------

for file in resume_folder.iterdir():

    if not file.is_file():
        continue

    # Extract text based on file type
    if file.suffix.lower() == ".pdf":
        resume_text = read_pdf(file)

    elif file.suffix.lower() == ".docx":
        resume_text = read_docx(file)

    else:
        print(f"Skipping unsupported file: {file.name}")
        continue

    # Create user prompt
    resume_user_prompt = f"""
Analyze the following resume and extract the required information.

Resume:
{resume_text}
"""

    resume_user_message = {
        "role": "user",
        "content": resume_user_prompt
    }

    messages = [
        resume_system_message,
        resume_user_message
    ]

    # Call LLM
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        response_format=response_format
    )

    # Convert JSON response into Resume object
    ans = response.choices[0].message.content
    data = json.loads(ans)

    resume = Resume(**data)

    # # Print extracted information
    # print("\n" + "=" * 60)
    # print(f"Resume: {file.name}")
    # print("=" * 60)
    # print("Name       :", resume.name)
    # print("Email      :", resume.email)
    # print("Skills     :", resume.skills)
    # print("Experience :", resume.experience)
    # print("Education  :", resume.education)
    # print("Projects   :", resume.projects)


class MatchResult(BaseModel):
    score: int
    matched_skills: list[str]
    missing_skills: list[str]
    reason: str

Match_schema = MatchResult.model_json_schema()

match_system_prompt = f"""
You are an experienced HR recruiter.

Your task is to compare a Job Description with a candidate's Resume.

Return ONLY valid JSON matching this schema:

{Match_schema}

Rules:
- Give an overall matching score between 0 and 100.
- Compare required skills with the candidate's skills.
- Compare preferred skills.
- Compare experience.
- Compare education.
- Compare projects only if they are relevant to the job.
- Mention which required skills are matched.
- Mention which required skills are missing.
- Give a short reason explaining the score.
- Do NOT invent information.
- Return ONLY valid JSON.
"""

match_system_message = {
    "role": "system",
    "content": match_system_prompt
}

#model_dump_json converts python objects into json as LLM doesnt understand python obj
comparison_user_prompt = f"""
Compare the following Job Description and Resume.

Job Description:
{jd.model_dump_json(indent=2)}

Resume:
{resume.model_dump_json(indent=2)}

Compare them carefully.

Return:
- score
- matched_skills
- missing_skills
- reason

Return ONLY valid JSON.
"""

comparison_user_message = {
    "role": "user",
    "content": comparison_user_prompt
}

messages = [
    match_system_message,
    comparison_user_message
]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=0,
    response_format=response_format
)

ans = response.choices[0].message.content

match_data = json.loads(ans)

match = MatchResult(**match_data)

print("\n" + "=" * 60)
print(f"Resume : {resume.name}")
print("=" * 60)
print("Score           :", match.score)
print("Matched Skills  :", match.matched_skills)
print("Missing Skills  :", match.missing_skills)
print("Reason          :", match.reason)