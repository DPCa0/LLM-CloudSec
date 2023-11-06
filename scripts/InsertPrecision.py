import pandas as pd
import json
import re

# Load the CSV file into a DataFrame
csv_file_path = 'dataset/sampled_vulnerable_codes.csv'
vulnerable_codes_df = pd.read_csv(csv_file_path)

# Load the JSON file into a list of dictionaries
json_file_path = 'flaw_predicted.json'
with open(json_file_path, 'r') as json_file:
    predicted_flaw_data = json.load(json_file)


def clean_comments(code_snippet):
    # Split the code snippet by lines
    lines = code_snippet.strip().split('\n')

    cleaned_lines = []
    for line in lines:
        # Remove content between /* ... */ but retain code outside them
        if '/*' in line and '*/' in line:
            start, _, end = line.partition('/*')
            _, _, after_end = end.partition('*/')
            line = start + after_end

        cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)


# Function to extract the code snippet following the /* FLAW */ comment
def extract_vulnerable_code_snippet(function_code):
    # Split the code into lines
    lines = function_code.split('\n')
    if '/*' not in function_code and '*/' not in function_code:
        return function_code
    # Find the lines with /* FLAW */ comment and extract the following code snippet
    snippet = ''
    capture = False
    for line in lines:
        if capture and line.strip() not in snippet:
            snippet += line + '\n'
            capture = False
        if '/*' in line:  # Check if line contains the comment indicating the start of a flaw
            snippet += line + '\n'
        if '*/' in line:  # Check if line contains the end of a comment
            capture = True

    return snippet


# Function to check if the predicted code intersects with the actual vulnerable code
def does_code_intersect(predicted_code, actual_code):
    # Split the predicted_code string into individual lines and strip whitespace.
    predicted_lines = [line.strip() for line in predicted_code.split('\n') if line.strip()]
    # If actual_code is a string, split it into lines as well.
    # Otherwise, if it's already a list or set of lines, this step is not needed.
    actual_lines = [line.strip() for line in actual_code.split('\n') if line.strip()]

    # Check each predicted line against each line in the actual code.
    for predicted_line in predicted_lines:
        for actual_line in actual_lines:
            # Check if the predicted line is a substring of the actual line.
            if predicted_line in actual_line or actual_line in predicted_line:
                return True  # Return True if a substring match is found.

    # Return False if no substring matches are found.
    return False


# Now let's apply these functions and check each prediction
correct_predictions = 0
incorrect_predictions = 0

for prediction in predicted_flaw_data:
    uid = int(prediction['UID'])
    predicted_code = prediction['predicted_flaw_code']
    # Extract the actual vulnerable code snippets for this UID from the CSV data
    actual_code_snippets = extract_vulnerable_code_snippet(vulnerable_codes_df[vulnerable_codes_df['UID'] == uid]['Function'].iloc[0])
    # Check for intersection between predicted and actual code snippets
    if does_code_intersect(predicted_code, actual_code_snippets):
        correct_predictions += 1
        with open("results.txt", "a") as f:
            f.write(f'Correct prediction\n {uid} \n{predicted_code} and\n {actual_code_snippets}\n')

    else:
        incorrect_predictions += 1
        with open("results.txt", "a") as f:
            f.write(f'Incorrect prediction\n {uid} \n{predicted_code} and\n {actual_code_snippets}\n')

# Display the result
print(f'Correct Predictions: {correct_predictions}')
print(f'Incorrect Predictions: {incorrect_predictions}')
