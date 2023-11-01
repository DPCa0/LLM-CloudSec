import json
import re

# Load the initial data
with open("predicted.json", "r") as file:
    data = json.load(file)

# Remove C-style comments
def remove_comments(code):
    # Multi-line comments
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    # Single-line comments
    code = re.sub(r'//.*', '', code)
    return code.strip()

# Process each value in the data
for value in data:
    value['code'] = remove_comments(value['code'])
    print(value['code'])
    pattern = value['code'].split('\n')[0]
    value['code'] = value['code'].replace(pattern, 'void test_snippet()')

# If you want to save the cleaned data back to the file
with open("predicted_filtered_output.json", "w") as file:
    json.dump(data, file, indent=4)
