from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

# client=genai.Client(api_key=os.getenv("API_KEY_FOR_QUESTION_EMBEDDING"))
client = OpenAI(
  api_key=os.getenv("API_KEY_FOR_QUESTION_EMBEDDING"),
  base_url="https://integrate.api.nvidia.com/v1"
)

def create_embedding(text):
    # r = requests.post(
    #     "http://localhost:11434/api/embeddings",
    #     json={
    #         "model": "bge-m3",
    #         "prompt": text
    #     }
    # )
    # return r.json()["embedding"]
#     result = client.models.embed_content(      #in order to deploy
#         model="gemini-embedding-2",
#         contents=text,
#         config=types.EmbedContentConfig(output_dimensionality=1024)
#    )

#     return result.embeddings[0].values
    res=client.embeddings.create(
        input=text,
        model="nvidia/nv-embed-v1",
        encoding_format="float",
        extra_body={"input_type": "query", "truncate": "NONE"}
       )

    return res.data[0].embedding

# print(create_embedding("Who is Napolean"))    