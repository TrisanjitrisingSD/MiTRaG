import os
import joblib
from dotenv import load_dotenv

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct

load_dotenv()

client = QdrantClient(
    url=os.getenv("QUAD_URL"),
    api_key=os.getenv("QUAD_API_KEY")
)

COLLECTION_NAME = "mitrag"

# Load dataframe
df = joblib.load("data/New_Embeddings.joblib")

print(df.shape)

# Create collection (only once)
try:
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=4096,
            distance=Distance.COSINE
        )
    )
    print("Collection created.")
except Exception:
    print("Collection already exists.")

BATCH_SIZE = 100
points = []

for i, (_, row) in enumerate(df.iterrows(), start=1):

    points.append(
        PointStruct(
            id=int(row["chunk_id"]),
            vector=row["embedding"],
            payload={
                "chunk_id": int(row["chunk_id"]),
                "number": int(row["number"]),
                "title": row["title"],
                "start": float(row["start"]),
                "end": float(row["end"]),
                "text": row["text"]
            }
        )
    )

    if len(points) >= BATCH_SIZE:

        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )

        print(f"Uploaded {i}/{len(df)} vectors")

        points = []

# Upload remaining vectors
if points:

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(f"Uploaded {len(df)}/{len(df)} vectors")

print("✅ Upload completed successfully.")