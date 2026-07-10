import joblib
import json
import pandas as pd


data=[]
with open('New_CombinedList_Of_Embedded_Chunks.json', 'r') as f:
    data = json.load(f)


df = pd.DataFrame.from_records(data)

joblib.dump(df,'New_Embeddings.joblib')