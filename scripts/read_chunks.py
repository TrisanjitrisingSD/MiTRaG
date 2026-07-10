import os
import json
import requests

def create_embedding(text_list,batch_size=100):
    embeddings = []
    for i in range(0, len(text_list), batch_size):
        r = requests.post("http://localhost:11434/api/embed", json={
            "model": "bge-m3",
            "input": text_list[i:i + batch_size]
        })
        # print("Status:", r.status_code)
        response = r.json()
        if "embeddings" not in response:
            raise RuntimeError(
                f"Batch {i//batch_size + 1} failed.\n"
                f"Status: {r.status_code}\n"
                f"Response: {response}"
            )
        # print(response)
        embeddings.extend(response["embeddings"])
    return embeddings


# a = create_embedding("Cat sat on the mat")
# print(a)
jsons=sorted(os.listdir("newjsons"))
my_dict = []
chunk_id=0
fileName=""
processed=False
for json_file in jsons:
    with open(f"newjsons/{json_file}", "r") as f:
        data = json.load(f)
    fileName=f"lecture_{json_file.split('_')[0]}.json"    
    if(os.path.exists(f"New_Embedded_jsons/{fileName}")):
        print(f"File {fileName} already exists with {len(data['chunks'])} chunks. Skipping.")
        chunk_id += len(data['chunks'])
        continue
    print(f"Processing {json_file} with {len(data['chunks'])} chunks")   
    processed=True
    # embeddings = create_embedding([chunk['text'] for chunk in data['chunks']])   
    texts=[chunk['text'] for chunk in data['chunks']]
    embeddings = create_embedding(texts,batch_size=100) 
    assert len(embeddings) == len(texts), (
    f"Expected {len(texts)} embeddings, got {len(embeddings)}"
    )
    for i, chunk in enumerate(data['chunks']):
        chunk['chunk_id'] = chunk_id
        chunk['embedding'] = embeddings[i]
        my_dict.append(chunk)
        chunk_id += 1  
    print(f"Processed {len(data['chunks'])} chunks from {json_file}")   
if processed:
    with open(f"New_Embedded_jsons/{fileName}", "w") as f:
        json.dump(my_dict, f)
    print("completed")
else:
    print("No new files to process.All Lectures have been processed and embedded. Please check the New_Embedded_jsons folder for the output files.")  

# total chunks processed= 25702(previously)
#total chunks processed=5152(after merging chunks)