from embedding_utils import create_embedding
from dotenv import load_dotenv
from qdrant_client import QdrantClient
import os
import json

load_dotenv()

client = QdrantClient(
    url=os.getenv("QUAD_URL"),      
    api_key=os.getenv("QUAD_API_KEY")
)

COLLECTION_NAME = "mitrag"


def prompt_create(question):

    question_embedding = create_embedding(question)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=question_embedding,
        limit=30
    )

    retrieved = []

    for hit in results.points:

        retrieved.append({
            "title": hit.payload["title"],
            "number": hit.payload["number"],
            "text": hit.payload["text"],
            "start": hit.payload["start"],
            "end": hit.payload["end"]
        })

    prompt = f"""
    You are an AI Teaching Assistant for the MIT OpenCourseWare Python Programming course.

    Below is the retrieved course material that you should use to answer the user's question.

    Retrieved Course Content:
    {json.dumps(retrieved, indent=2)}

    ------------------------------------------------------------

    User Question:
    {question}

    ------------------------------------------------------------

    Instructions:

    - Answer ONLY using the information available in the retrieved course content.
    - If the question is outside the scope of the MIT Python course and if it is not simple greetings or "ok" or "Thanks", politely reply:
    "I can only answer questions related to the MIT OpenCourseWare Python Programming course."
    otherwise reply "If you have further queries, feel free to ask. Thanks"
    - Explain concepts in a beginner-friendly and conversational manner.
    - Keep the explanation concise (around 150-250 words unless the user asks for more detail).
    - Do NOT mention transcript chunks, JSON, retrieved context, embeddings, or internal implementation.
    - Do NOT ask follow-up or counter questions.
    - Avoid unnecessary repetition.
    - Use Markdown formatting.
    - Use short paragraphs (2-3 lines maximum).
    - Use bullet points wherever appropriate.
    - Use emojis only for section headings (avoid excessive emojis).

    If code is helpful, include a short Python example.

    At the end, add a section exactly like this:

    ---

    ## 📚 Related Lectures

    🎥 **Lecture <number> – <title>**
    ⏱ <start time> – <end time>

    (Include at most 3 lectures.)

    Only include lectures that are directly relevant to the answer.

    Convert timestamps into MM:SS or HH:MM:SS format.

    ------------------------------------------------------------

    Example output:

    # 🔁 Recursion

    Recursion is a programming technique where a function solves a problem by calling itself with a smaller version of the same problem.

    Every recursive function has two essential parts:

    - **Base Case** – Stops the recursion.
    - **Recursive Case** – Calls itself with a smaller input.

    Example:

    ```python
    def factorial(n):
        if n == 0:
            return 1
        return n * factorial(n - 1)"""
    
    return prompt


# print(prompt_create("Who is Napolean?")) # testing purpose