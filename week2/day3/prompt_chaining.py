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

JD="""
We are hiring a Backend Python Developer.

Requirements:
- Strong Python
- FastAPI or Django
- PostgreSQL
- Docker
- AWS
- REST APIs
- 2+ years of experience
"""
resume="""
Name: Rahul Sharma

Experience:
3 years as a Software Developer.

Skills:
Python, FastAPI, MySQL, Docker,
REST APIs, Git

Projects:
Built a food delivery backend using
FastAPI and MySQL.

Deployed applications using Docker.
"""

def ask_llm(system_prompt,user_prompt):
    system_message={
        "role":"system",
        "content":system_prompt
    }
    user_message={
        "role":"user",
        "content":user_prompt
    }
    messages=[system_message,user_message]
    response=client.chat.completions.create(model=model,temperature=0,messages=messages)
    ans=response.choices[0].message.content
    return ans

def extract_resume():
    system_prompt="""
    You are a professional HR assistant. Extarct the skills from the candidates resume provided.
    Only return the no other information.
    Do not invent skills by yourself
    Output Format:
    Skills should be separated by commas. Just return comma separated skills do not return any other filler information
    """
    user_prompt=f"""
    Extarct the skills from this resume.
    {resume}
    """
    return ask_llm(system_prompt,user_prompt)

def extract_jd():
    #Extract Skills from resume
    system_prompt="""
    You are a professional HR assistant. Extarct the skills from the candidates Job Description provided.
    Only return the no other information.
    Do not invent skills by yourself
    Output Format:
    Skills should be separated by commas. Just return comma separated skills do not return any other filler information
    """
    user_prompt=f"""
    Extarct the skills from this resume.
    {JD}
    """
    return ask_llm(system_prompt,user_prompt)

def match_scores(JD,candidate):
    system_prompt="""
    You are a professional HR assistant. Compare the skills of candidate and the skills required in Job Description and produce a final score between 1 and 100 and also produce a final verdict in short weather a candidate is a good fit for a role or not.
    """
    user_prompt=f"""
    Compare and match the skills.
    JD:
    {JD}
    Candidate:
    {candidate}
    """

    return ask_llm(system_prompt,user_prompt)

candidate=extract_resume()
job_desc=extract_jd()

score=match_scores(candidate,job_desc)

print(score)   



