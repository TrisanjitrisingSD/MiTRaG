from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

client=genai.Client(api_key=os.getenv("API_KEY_FOR_QUESTION_EMBEDDING"))

def create_embedding(text):
    # r = requests.post(
    #     "http://localhost:11434/api/embeddings",
    #     json={
    #         "model": "bge-m3",
    #         "prompt": text
    #     }
    # )
    # return r.json()["embedding"]
    result = client.models.embed_content(      #in order to deploy
        model="gemini-embedding-2",
        contents=text,
        config=types.EmbedContentConfig(output_dimensionality=1024)
   )

    return result.embeddings[0].values

# print(create_embedding("Who is Napolean"))    