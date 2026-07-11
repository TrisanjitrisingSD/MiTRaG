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


def format_time(seconds):
    seconds = int(seconds)

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours:
        return f"{hours:02}:{minutes:02}:{secs:02}"
    else:
        return f"{minutes:02}:{secs:02}"


def prompt_create(question):

    question_embedding = create_embedding(question)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=question_embedding,
        limit=50
    )

    retrieved = []

    for hit in results.points:

        retrieved.append({
            "title": hit.payload["title"].replace("_", " "),
            "number": hit.payload["number"],
            "text": hit.payload["text"],
            "start": format_time(hit.payload["start"]),
            "end": format_time(hit.payload["end"])
        })
        if not results.points:
            return None
        best_score = results.points[0].score
        if best_score < 0.30:
            return None
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

        - Answer ONLY using the retrieved course content.
        - If the question is outside the MIT Python course (excluding greetings like "Hi", "Thanks", "OK"), reply:

        "I can only answer questions related to the MIT OpenCourseWare Python Programming course."
         And Donot answer anything,if this happens 

        - For greetings or thanks, politely reply:
        "If you have further queries, feel free to ask. Thanks."

        - Explain concepts in a beginner-friendly manner.
        - Keep answers concise (150–250 words unless asked otherwise).
        - Never mention transcript chunks, embeddings, retrieval, JSON, or internal implementation.
        - Do not ask follow-up questions.
        - Use Markdown.
        - Use short paragraphs.
        - Use bullet points where appropriate.
        - Include a short Python example whenever useful.

        At the end include:

        ---

        ## 📚 Related Lectures

        🎥 **Lecture <number> – <title>**
        ⏱ <start> – <end>

        Include at most 3 lectures.

        Use ONLY the lectures present in the retrieved course content.
        Do NOT invent lecture names or timestamps.
        The timestamps are already formatted. Copy them exactly.

        ------------------------------------------------------------
        """

    return prompt