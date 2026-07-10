from google import genai
from dotenv import load_dotenv
import os
load_dotenv()
client=genai.Client(api_key=os.getenv("API_KEY"))
import requests
from create_prompt import prompt_create

def llama_answer(prompt):
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False,
        }
    )
    response = r.json()
    return response["response"]


def gemini_answer(prompt):
    responsE = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return responsE.text


def ask_llm(question):
    prompt=prompt_create(question)
    try:

        answer = gemini_answer(prompt)

        return {
        "answer": answer,
        "model": "Gemini"
    }

    except Exception as e:
        print("Gemini Error",e)
        # answer = llama_answer(prompt) not possible during deployment 
        answer="Server is Busy With Other Query"
        return {
            "answer":"Quota Exhausted for retrival,Plz try again later",
            "model":"Gemini"
        }