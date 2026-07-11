import base64
import os
import json
import joblib
import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from google import genai
from dotenv import load_dotenv

load_dotenv()

client=genai.Client(os.getenv("API_GEMINI_EMBEDDING"))

def create_embedding(text):
    r = requests.post(
        "http://localhost:11434/api/embeddings",
        json={
            "model": "bge-m3",
            "prompt": text
        }
    )
    return r.json()["embedding"]
    

   
# for querying to the LLM

def inference(prompt):
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False,
        }
    )
    response = r.json()
    return response


def gemini_inference(prompt):
    responsE = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return responsE.text

df=joblib.load('data/New_Embeddings.joblib')

incoming_query=input("Enter your query: ")
question_embedding=create_embedding(incoming_query)

similarity_scores = cosine_similarity(np.vstack(df['embedding']),[question_embedding]).flatten()
# print(similarity_scores)

top_results=50

max_indx=similarity_scores.argsort()[::-1][0:top_results]

new_df=df.loc[max_indx]

# for index,item in new_df.iterrows():
#     print(index,item["title"],item["number"],item["text"],item["start"],item["end"])


prompt=f'''
   Python is being taught in MIT_OPENCOURSEWARE.Here are video subtitle chunks from the course containing video title,video number,start time in seconds,
   end time in seconds , the text at that time:
   
   {new_df[["title","number","text","start","end"]].to_json(orient="records")}
   ------------------------------------------------
   "{incoming_query}"
    User asked this question related to the video chunks,You are a helpful assistant to answer(in a human way and and donot mention the above format, it is just for your reference) where and how much content is taught in which video(in which video and at what timestamp)
    and guide the user to go to that particular video.If user asks unrelated question,tell the user that you can only answer
    questions related to the course.       
    And,Donot ask counter questions to the user,just answer the question in a human way and provide the answer in a human way.                                               
'''

with open("prompt.txt", "w") as f:
    f.write(prompt)

response1 = inference(prompt)["response"]

try:
    response2 = gemini_inference(prompt)
except Exception as e:
    print(f"Gemini Error: {e}")
    response2 = "Server is Busy."

with open("response.txt", "w", encoding="utf-8") as f:
    f.write(f"Response from LLAMA:\n{response1}\n\n")
    f.write(f"Response from Gemini:\n{response2}")
print(response1)
print("Query is Done")