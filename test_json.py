import json

with open('predicted.json', 'r') as f:
    data = json.load(f)
print(len(data))
