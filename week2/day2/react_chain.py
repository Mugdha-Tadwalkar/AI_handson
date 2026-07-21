import os
from pathlib import Path
from time import sleep
from dotenv import load_dotenv
from groq import Groq
import re

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client=Groq(api_key=my_api_key)
model="llama-3.3-70b-versatile"

def check_warranty(serial_number):
    warranty_data = {
        "ABC123": "Under Warranty",
        "XYZ456": "Warranty Expired",
        "PQR789": "Under Warranty",
        "LMN111": "Warranty Expired"
    }

    return warranty_data.get(
        serial_number,
        "Serial Number Not Found"
    )


def repair_cost(problem):
    problem = problem.lower()

    if "screen" in problem:
        return 6000

    elif "battery" in problem:
        return 2500

    elif "speaker" in problem:
        return 1800

    elif "camera" in problem:
        return 5000

    elif "charging" in problem:
        return 1500

    else:
        return 1000


def service_center(city):
    centers = {
        "bangalore": "Koramangala Service Center",
        "mumbai": "Andheri Service Center",
        "pune": "Shivaji Nagar Service Center",
        "hyderabad": "Madhapur Service Center",
        "delhi": "Connaught Place Service Center"
    }

    return centers.get(
        city.lower(),
        "No Service Center Found"
    )


def calculator(expression):
    try:
        return eval(expression)
    except:
        return "Calculation Error"

tools={
    "check_warranty":check_warranty,
    "repair_cost":repair_cost,
    "service_center":service_center,
    "calculator":calculator
}

system_prompt="""
You are an AI support assistant at Laptop Service Centre.

Your task is to answer user questions by using following tools:

check_warranty
repair_cost
service_center
calculator

Understand user's question and the data in the question like serial number, city, issue.
Depending on that data call the specific tool.
Do not hallicunate.
Follow these rules:

1. Decide what you need to do next.
2. Call ONLY ONE tool at a time.
3. After writing an Action, STOP immediately.
4. Never guess or invent a tool result.
5. Wait until you receive an Observation.
6. Then decide your next action.
7. When the task is complete, give the Final Answer.

Format:

Thought: what you need to do
Action: tool_name(argument)

When finished:

Final Answer: your answer

"""

import re
from time import sleep

def run_agent(question):

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(5):

        print("\n" + "-" * 50)
        print(f"STEP {step + 1}")
        print("-" * 50)

        # Call LLM
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
        )

        answer = response.choices[0].message.content

        print(answer)

        # Stop if LLM has finished
        if "Final Answer:" in answer:
            break

        # Find Action
        match = re.search(
            r'Action:\s*(\w+)\((.*?)\)',
            answer
        )

        if not match:
            print("No Action found.")
            break

        tool_name = match.group(1)
        tool_input = match.group(2).strip().strip('"')

        print("\nTool Name :", tool_name)
        print("Tool Input:", tool_input)

        # Execute Tool
        if tool_name in tools:

            tool = tools[tool_name]

            observation = tool(tool_input)

        else:

            observation = "Tool not found"

        print("Observation:", observation)

        # Save assistant response
        messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        # Send observation back to LLM
        messages.append(
            {
                "role": "user",
                "content": f"Observation: {observation}"
            }
        )

        sleep(2)

prompt="""

My laptop serial number is ABC12367.
The battery is damaged.
I live in Delhi.
How much will the repair cost?

"""
run_agent(prompt)