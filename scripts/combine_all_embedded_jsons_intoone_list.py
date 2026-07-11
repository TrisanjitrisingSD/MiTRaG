import os
import json

my_list = []

files = sorted(os.listdir("transcripts/New_Embedded_jsons"))

for file in files:
    with open(f"transcripts/New_Embedded_jsons/{file}", "r") as f:
        data = json.load(f)
    for ele in data:
        my_list.append(ele)

with open("data/New_CombinedList_Of_Embedded_Chunks.json", "w",encoding="utf-8") as f:
    json.dump(my_list, f, indent=4, ensure_ascii=False)

print(f"Combined {len(my_list)} embedded chunks.")