import joblib
import numpy as np
import time
import pandas as pd
import json
from sklearn.metrics.pairwise import cosine_similarity
from embedding_utils import create_embedding

OLD_FILE = "data/Embeddings.joblib"
NEW_FILE = "data/New_Embeddings.joblib"

TOP_K = 50


def evaluate(df, question):

    q_embedding = create_embedding(question)

    start = time.perf_counter()

    scores = cosine_similarity(
        np.vstack(df["embedding"]),
        [q_embedding]
    ).flatten()

    idx = scores.argsort()[::-1][:TOP_K]

    retrieval_time = (time.perf_counter() - start) * 1000

    retrieved = df.iloc[idx]

    top_scores = scores[idx]

    total_words = retrieved["text"].str.split().str.len().sum()

    avg_words = retrieved["text"].str.split().str.len().mean()

    return {
        "time": retrieval_time,
        "top1_similarity": float(top_scores[0]),
        "top5_similarity": float(np.mean(top_scores[:5])),
        "total_words": int(total_words),
        "avg_words": float(avg_words)
    }


def main():

    print("Loading embeddings...")

    old_df = joblib.load(OLD_FILE)
    new_df = joblib.load(NEW_FILE)

    with open("data/benchmark_questions.json", "r", encoding="utf-8") as f:
        benchmark = json.load(f)

    results = []

    print()

    for item in benchmark:

        q = item["question"]

        print(f"Running Q{item['id']}...")

        old = evaluate(old_df, q)
        new = evaluate(new_df, q)

        results.append({

            "ID": item["id"],
            "Question": q,

            "Old Time(ms)": old["time"],
            "New Time(ms)": new["time"],

            "Old Top1": old["top1_similarity"],
            "New Top1": new["top1_similarity"],

            "Old Top5": old["top5_similarity"],
            "New Top5": new["top5_similarity"],

            "Old Context Words": old["total_words"],
            "New Context Words": new["total_words"],

            "Old Avg Chunk Words": old["avg_words"],
            "New Avg Chunk Words": new["avg_words"]
        })

    df = pd.DataFrame(results)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    reduction = (1 - len(new_df) / len(old_df)) * 100

    print(f"\nOld vectors               : {len(old_df)}")
    print(f"New vectors               : {len(new_df)}")
    print(f"Vector Reduction          : {reduction:.2f}%")

    print()

    old_time = df["Old Time(ms)"].mean()
    new_time = df["New Time(ms)"].mean()

    print("Average Retrieval Time")

    print(f"Old                       : {old_time:.2f} ms")
    print(f"New                       : {new_time:.2f} ms")

    print(f"Improvement               : {((old_time-new_time)/old_time)*100:.2f}%")

    print()

    print("Average Top-1 Similarity")

    print(f"Old                       : {df['Old Top1'].mean():.4f}")
    print(f"New                       : {df['New Top1'].mean():.4f}")

    print()

    print("Average Top-5 Similarity")

    print(f"Old                       : {df['Old Top5'].mean():.4f}")
    print(f"New                       : {df['New Top5'].mean():.4f}")

    print()

    print("Average Retrieved Context")

    print(f"Old                       : {df['Old Context Words'].mean():.0f} words")

    print(f"New                       : {df['New Context Words'].mean():.0f} words")

    increase = (
        (df["New Context Words"].mean() -
         df["Old Context Words"].mean())
        / df["Old Context Words"].mean()
    ) * 100

    print(f"Increase                  : {increase:.2f}%")

    print()

    print("Average Chunk Size")

    print(f"Old                       : {df['Old Avg Chunk Words'].mean():.1f} words")

    print(f"New                       : {df['New Avg Chunk Words'].mean():.1f} words")

    df.to_csv("comparison_results.csv", index=False)

    print("\nSaved comparison_results.csv")


if __name__ == "__main__":
    main()    