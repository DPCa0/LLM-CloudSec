import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from utils.ask import *
from model.prompt import *
from model.code import *
import csv
import os
import json
import re


def clean_code(code_snippet):
    # Split the code snippet by lines
    lines = code_snippet.strip().split('\n')

    # Extract the function title from the last part of the first line
    title = lines[0].split(' ')[-1].strip().replace('()', '')

    cleaned_lines = []
    for line in lines:
        # Replace the function title in the line
        line = line.replace(title, 'test_snippet')

        # Remove content between /* ... */ but retain code outside them
        if '/*' in line and '*/' in line:
            start, _, end = line.partition('/*')
            _, _, after_end = end.partition('*/')
            line = start + after_end

        cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)


def classification(query, temperature: float = 0.01):
    system_prompt = make_msg('system', classify_empty_prompt)
    message = make_msg('user', query)
    content = openai_ask(message, model_name='gpt-4', history=system_prompt, temperature=temperature)
    print(f"判断结果：{content}")
    return content


def load_test_data(filename):
    # Extract data using csv.reader
    extracted_data_text = []

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Skip the header

        for row in reader:
            try:
                extracted_data_text.append((row[0], row[1], row[2]))
            except IndexError:
                # This will catch any rows that don't have the expected number of columns
                extracted_data_text.append((f"Malformed row: {row}",))

    # Display the extracted data (or you can return it if needed)
    for data in extracted_data_text:
        print(data)

    return extracted_data_text


def get_predicted_labels(data, cache_file='D2A_cache_cleaned.json'):
    # Step 1: Check if a cache file exists
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache_content = json.load(f)
            if isinstance(cache_content, dict):  # ensure cache content is a dictionary
                cache = cache_content
            else:
                cache = {}
    else:
        cache = {}

    predicted = []

    for item in data:
        # Step 3: If UID is found in the cache, skip processing
        uid_str = str(item[0])  # convert UID to string
        if uid_str in cache:
            predicted.append(cache[uid_str])
            continue

        cleaned_code = clean_code(item[2])
        label = classification(cleaned_code)
        entry = {
            'ID': item[0],
            'UID': item[1],
            'code': cleaned_code,
            'predicted': label
        }
        predicted.append(entry)

        # Step 4: Update the cache and save to the file
        cache[uid_str] = entry
        with open(cache_file, 'w') as f:
            json.dump(cache, f)

    return predicted


def extract_cwe_data():
    # Read the file as a normal text file and split each line by comma
    with open('dataset/matched_cwe_data.csv', 'r') as file:
        lines = file.readlines()

    # Extract the headers and data
    headers = lines[0].strip().split(',')
    datas = [line.strip().split(',') for line in lines[1:]]

    # Extract the first and second columns
    extracted_data_text = [(line[0], line[1]) for line in datas]
    for data in extracted_data_text:
        description = data[1].replace('"', '')
        print(f"{data[0]},{description}")


data = load_test_data('dataset/sampled_vulnerable_codes.csv')
predicted = get_predicted_labels(data)
with open('empty_predicted.json', 'w') as f:
    json.dump(predicted, f)





# # Extracting true_labels and predicted_labels from the dataset
# true_labels = data["CWE"].values
# predicted_labels = get_predicted_labels()
#
# # Convert predicted labels to category codes for metrics calculations
# predicted_labels_codes = pd.Categorical(predicted_labels, categories=sorted(data["CWE"].unique())).codes
#
# # Number of unique CWE categories
# num_cwe_categories = len(data["CWE"].unique())
# cwe_labels = sorted(data["CWE"].unique())
#
# # Accuracy
# accuracy = accuracy_score(true_labels, predicted_labels)
# print(f"Accuracy: {accuracy:.4f}")
#
# # Classification Report (Precision, Recall, F1-Score)
# report = classification_report(true_labels, predicted_labels_codes, target_names=cwe_labels, zero_division=0)
# print(report)
#
# # Confusion Matrix
# conf_matrix = confusion_matrix(true_labels, predicted_labels_codes)
#
# # Plotting confusion matrix
# plt.figure(figsize=(15, 15))
# plt.imshow(conf_matrix, interpolation='nearest', cmap=plt.cm.Blues)
# plt.title("Confusion Matrix")
# plt.colorbar()
# tick_marks = np.arange(num_cwe_categories)
# plt.xticks(tick_marks, cwe_labels, rotation=90)
# plt.yticks(tick_marks, cwe_labels)
# plt.tight_layout()
# plt.ylabel('True label')
# plt.xlabel('Predicted label')
# plt.show()
