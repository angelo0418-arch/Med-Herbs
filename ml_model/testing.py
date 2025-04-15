import json

with open("class_indices.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Check total count
print("Total herbs:", len(data))

# Check if all indices are sequential
for i in range(len(data)):
    if str(i) not in data:
        print(f"Missing index: {i}")
