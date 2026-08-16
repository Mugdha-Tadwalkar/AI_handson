import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq
from pypdf import PdfReader


# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set")


# ---------------------------------------------------------
# Groq client
# ---------------------------------------------------------

client = Groq(api_key=GROQ_API_KEY)

MODEL = "llama-3.3-70b-versatile"


# ---------------------------------------------------------
# Resume path
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

RESUME_PATH = BASE_DIR / "Resume" / "MugdhaTadwalkar_CV.pdf"


# ---------------------------------------------------------
# Read resume
# ---------------------------------------------------------

def read_resume() -> str:

    if not RESUME_PATH.exists():
        raise FileNotFoundError(
            f"Resume not found at: {RESUME_PATH}"
        )

    reader = PdfReader(str(RESUME_PATH))

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    if not text.strip():
        raise ValueError("Could not extract text from the resume")

    return text.strip()


# ---------------------------------------------------------
# Load resume once when application starts
# ---------------------------------------------------------

resume_text = read_resume()


# ---------------------------------------------------------
# System prompt
# ---------------------------------------------------------

chatbot_system_prompt = f"""
You are Mugdha Tadwalkar's AI Portfolio Assistant.

Your job is to answer questions about Mugdha using ONLY the
information contained in her resume below.

================ RESUME ================

{resume_text}

============== END RESUME ==============


IMPORTANT RULES:

1. Answer ONLY using information explicitly available in the resume.

2. Never invent, assume, or guess information.

3. If the requested information is not present in the resume,
   respond with exactly:

   "This information is not available in the resume."

4. You can answer questions about:
   - Education
   - Degree
   - College
   - Work experience
   - Companies
   - Roles
   - Projects
   - Skills
   - Programming languages
   - AI technologies
   - LLMs
   - RAG
   - Agentic AI
   - Backend technologies
   - Databases
   - Cloud technologies
   - Certifications
   - Location
   - Professional summary

5. If the user asks a question such as:
   "What is your education?"
   "Where did Mugdha study?"
   "What degree does she have?"
   "Where does she work?"
   "What projects has she worked on?"

   Answer directly from the resume.

6. Do not return JSON.

7. Keep answers concise and conversational.

8. If the user asks multiple questions, answer all of them
   using only information available in the resume.

9. Refer to the candidate naturally as "Mugdha" or "she".

10. Do not claim that Mugdha has experience with a technology
    unless that technology appears in the resume.
"""


# ---------------------------------------------------------
# Answer user question
# ---------------------------------------------------------

def answer_question(question: str) -> str:

    if not question or not question.strip():
        return "Please ask me a question about Mugdha."

    try:

        response = client.chat.completions.create(

            model=MODEL,

            messages=[
                {
                    "role": "system",
                    "content": chatbot_system_prompt
                },
                {
                    "role": "user",
                    "content": question.strip()
                }
            ],

            temperature=0

        )

        answer = response.choices[0].message.content

        if not answer:
            return "Sorry, I could not generate an answer."

        return answer.strip()

    except Exception as e:

        print("Groq API Error:", e)

        return "Sorry, I could not process your question right now."