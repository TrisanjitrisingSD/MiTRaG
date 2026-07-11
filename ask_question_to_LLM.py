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
    api_key=os.getenv("API_KEY_FOR_QUESTION"),
    timeout=30
)
GENERAL_CHAT = {
    "what's your name",
    "what is your name",
    "who are you",
    "how are you",
    "who made you",
    "tell me a joke",
    "good morning",
    "good evening",
    "good night",
    "hello",
    "hi",
    "hey",
    "thanks",
    "thank you",
    "thanku",
    "bye",
    "goodbye"
}

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
    model="meta/llama-3.1-8b-instruct",
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
    max_tokens=1024,
   )
    answer = response.choices[0].message.content
    return answer

def ask_llm(question):
    q = question.lower().strip()
    if q=="ok":
        return{
            "answer":"Yeah!!",
            "model":"System"
        }
    if q=="thanks" or q=="thank you" or q=="Thanks" or q=="thanku":
            return{
                "answer":"Mention not!But ask me questions from the MIT OpenCourseWare only,I am not here for Casual Chat.",
                "model":"System"
            }
    if q in GENERAL_CHAT:
        return {
        "answer": "Hi! I'm MiTRaG, an AI tutor for the MIT OpenCourseWare Python Programming course. Feel free to ask me anything related to Python.",
        "model": "System"
        }
    prompt=prompt_create(question)
    prompt = prompt_create(question)

    if prompt is None:
        return {
            "answer": "I can only answer questions related to the MIT OpenCourseWare Python Programming course.",
            "model": "System"
        }
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
        
      