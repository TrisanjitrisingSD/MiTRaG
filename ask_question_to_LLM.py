from google import genai
from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv()
client1=genai.Client(api_key=os.getenv("API_KEY_GEMINI"))
import requests
from create_prompt import prompt_create

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("API_KEY_FOR_QUESTION")
)

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
    responsE = client1.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return responsE.text

def nvidia_answer(prompt):
   response = client.chat.completions.create(
    model="meta/llama-3.2-3b-instruct",
    messages=[
        {
            "role": "system",
            "content": "You are an MIT Python Teaching Assistant. Answer only using the provided context when possible."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.2,
    max_tokens=512,
   )
   answer = response.choices[0].message.content
   return answer

def ask_llm(question):
    prompt=prompt_create(question)
    try:
        answer=gemini_answer(prompt)
        return {
            "answer":answer,
            "model":"Gemini"
        }
    except Exception as e:
        print("Gemini Error",e)
        try:

            answer = nvidia_answer(prompt)

            return {
            "answer": answer,
            "model": "Nvidia"
        }

        except Exception as e:
            print("Nvidia Error",e)
            # answer = llama_answer(prompt) not possible during deployment 
            answer="Server is Busy With Other Query"
            return {
                "answer":"Quota Exhausted for retrieval,Plz try again later",
                "model":"Nvidia"
            }