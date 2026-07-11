import joblib
from embedding_utils import create_embedding
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from embedding_utils import create_embedding


df=joblib.load('data/New_Embeddings.joblib') 



def prompt_create(question):
    question_embedding=create_embedding(question)
    # print(len(question_embedding))
    # print(np.vstack(df["embedding"]).shape)
    similarity_scores = cosine_similarity(np.vstack(df['embedding']),[question_embedding]).flatten()

    top_results=50

    max_indx=similarity_scores.argsort()[::-1][0:top_results]

    new_df=df.loc[max_indx]


    prompt = f"""
        You are an AI Teaching Assistant for the MIT OpenCourseWare Python Programming course.

        Below is the retrieved course material that you should use to answer the user's question.

        Retrieved Course Content:
        {new_df[["title","number","text","start","end"]].to_json(orient="records")}

        ------------------------------------------------------------

        User Question:
        {question}

        ------------------------------------------------------------

        Instructions:

        - Answer ONLY using the information available in the retrieved course content.
        - If the question is outside the scope of the MIT Python course and if it is not simple greetings or "ok" or "Thanks", politely reply:
        "I can only answer questions related to the MIT OpenCourseWare Python Programming course."
         otherwise reply "If you have further queries,feel free to ask.Thanks"
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

    return prompt;        

print(prompt_create("What is Recursion?"))