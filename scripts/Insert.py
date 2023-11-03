import json
import re
import numpy as np
import csv
from utils.ask import *
from model.prompt import *
import os
import pickle


def integrated_json_parser(file_path):
    objects = []  # List to store all the parsed JSON objects
    current_object = {}  # Current object being parsed
    key = None  # Current key being parsed in the object
    value = None  # Current value being parsed for the key
    is_string = False  # Flag to indicate if we are currently parsing a string value
    escape_character = False  # Flag to indicate the last character was a backslash (escape character)
    reading_key = True  # Flag to indicate if we are currently reading a key

    with open(file_path, 'r') as file:
        while True:
            char = file.read(1)  # Read one character at a time
            if not char:
                # End of file
                if current_object:  # If there's an object being parsed, add it to the objects list
                    objects.append(current_object)
                break

            if reading_key:
                if char == '"':
                    if not key:
                        key = ""  # Start a new key
                    else:
                        reading_key = False  # End the current key
                elif key is not None:
                    key += char  # Add character to key
            else:
                if is_string:
                    if escape_character:
                        value += '\\' + char  # Add escaped character to value
                        escape_character = False
                    elif char == '\\':
                        escape_character = True  # Next character is escaped
                    elif char == '"':
                        is_string = False  # End of string
                    else:
                        value += char  # Add character to value
                else:
                    if char == ':':
                        value = ""  # Start a new value
                        is_string = True  # Next value will be a string
                    elif char == ',':
                        current_object[key] = value  # Add the key-value pair to the current object
                        key = None  # Reset key for next key-value pair
                        value = None  # Reset value for next key-value pair
                        reading_key = True  # Next characters will be a key
                    elif char == '{':
                        # Nested object starts, this requires a stack or recursion to handle correctly
                        pass
                    elif char == '}':
                        current_object[key] = value  # Add the last key-value pair to the current object
                        objects.append(current_object)  # Add the current object to the objects list
                        current_object = {}  # Reset current object for the next object
                        key = None  # Reset key for next object
                        value = None  # Reset value for next object
                        reading_key = True  # Next characters will be a key

    return objects


def insert(query, temperature: float = 0.01, prompt: str = insert_prompt):
    system_prompt = make_msg('system', prompt)
    message = make_msg('user', query)
    content = openai_ask(message, model_name='gpt-4', history=system_prompt, temperature=temperature)
    print(f"判断结果：{content}")
    return content


def get_description(cwe_id, file_path):
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        # Initializing the CSV reader
        reader = csv.reader(csvfile)

        # Getting the header
        header = next(reader)
        print(header)

        # Checking if 'CWE-ID', 'Description' and 'Extended Description' columns exist in the header
        if 'CWE-ID' not in header or 'Name' not in header or 'Description' not in header or 'Extended Description' not in header:
            raise ValueError("CSV doesn't have the necessary columns")

        # Iterating over rows to find the given CWE-ID
        for row in reader:
            if row[header.index('CWE-ID')] == str(cwe_id):
                return row[header.index('Name')], row[header.index('Description')], row[header.index('Extended Description')]

    return None, None, None


# Check if cache exists
try:
    with open("cache_D2A.pkl", "rb") as cache_file:
        new_data = pickle.load(cache_file)
except FileNotFoundError:
    new_data = []

# Load the initial data
with open("test_D2A.json", "r") as file:
    data = json.load(file)

# Find out where to start
start_index = len(new_data)

for index, value in enumerate(data[start_index:]):
    # Extract the numerical value from the CWE field
    # value['CWE'] = int(value['CWE'].split('CWE')[1])
    if isinstance(value, dict):
        predicted_value = value.get('predicted', None)
        if predicted_value is None:
            print(f"Skipping {value['UID']} because it doesn't have a predicted value")
            continue
        numbers = re.findall(r'(\d+)', predicted_value)
        name = []
        des = []
        des_extended = []

        for i in range(len(numbers)):
            name1 = get_description(numbers[i], 'dataset/matched_cwe_data.csv')[0]
            name.append(name1)
            des1 = get_description(numbers[i], 'dataset/matched_cwe_data.csv')[1]
            des.append(des1)
            des2 = get_description(numbers[i], 'dataset/matched_cwe_data.csv')[2]
            des_extended.append(des2)

        name = [item for item in name if item is not None]
        des = [item for item in des if item is not None]
        des_extended = [item for item in des_extended if item is not None]

        for i in range(len(name)):
            prompt_ = insert_prompt
            prompt_ = prompt_.replace("are:", "are:" + des_extended[i])
            prompt_ = prompt_.replace("are:", "are:" + des[i])
            prompt_ = prompt_.replace("are:", "are:" + name[i])
            prompt_ = prompt_.replace("are:", "are: CWE " + numbers[i] + " ")

        print(prompt_)
        flaw_code = insert(value['code'], prompt=prompt_)
        new_data.append({
            'UID': value['UID'],
            'code': value['code'],
            'predicted': value['predicted'],
            # 'CWE': value['CWE'],
            'prompt': prompt_,
            'predicted_flaw_code': flaw_code
        })

        # Update the cache
        with open("cache_D2A.pkl", "wb") as cache_file:
            pickle.dump(new_data, cache_file)

# Once done, save the final result and delete the cache
with open("flaw_predicted_D2A.json", "w") as file:
    json.dump(new_data, file, ensure_ascii=False, indent=2)

try:
    os.remove("cache_D2A.pkl")
except:
    pass
