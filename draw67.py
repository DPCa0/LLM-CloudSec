import json
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

# Function to extract CWE numbers from a string (predicted or actual CWE strings)
def extract_cwe_numbers(cwe_string):
    # CWE strings can contain multiple entries separated by '\n'
    entries = cwe_string.split('\n')
    cwe_numbers = []
    for entry in entries:
        # Each entry is of the form 'number,description'
        number = entry.split(',')[0]
        # We make sure that the extracted number is a digit before appending
        if number.isdigit():
            cwe_numbers.append(int(number))
    return cwe_numbers

# Function to extract a single CWE number from the actual CWE field
def extract_cwe_number(cwe_string):
    # CWE strings are assumed to be of the form 'CWE<number>'
    parts = cwe_string.split('CWE')
    if len(parts) > 1 and parts[1].isdigit():
        return int(parts[1])
    else:
        return None

# Load the JSON data from the uploaded file
file_path = 'modified_predicted_filtered_output.json'

with open(file_path, 'r') as file:
    data = json.load(file)

# Dictionary to hold the correct counts of CWE occurrences
correct_cwe_counts = defaultdict(int)

# Iterate through each item in the dataset
for item in data:
    # Extract the actual CWE number
    actual_cwe_number = extract_cwe_number(item['CWE'])
    # If an actual CWE number was found
    if actual_cwe_number:
        # Extract predicted CWE numbers
        predicted_cwe_numbers = extract_cwe_numbers(item['predicted'])
        # If the actual CWE number is in the predicted numbers, count it as correct
        if actual_cwe_number in predicted_cwe_numbers:
            correct_cwe_counts[actual_cwe_number] += 1

# Sort the dictionary by key (CWE number) to ensure we have an ordered representation
sorted_correct_cwe_counts = dict(sorted(correct_cwe_counts.items()))

# Increase figure width to provide more space for bars
plt.figure(figsize=(12, 10))

# Use smaller font size for y-ticks to prevent overlapping
ytick_font_size = 8

# Calculate the step size for y-ticks
step_size = int(np.ceil(len(sorted_correct_cwe_counts) / 67))

# Create a list of y-ticks that will actually be displayed
y_ticks = list(range(0, len(sorted_correct_cwe_counts), step_size))

# Create a list of labels for the y-axis with most set to empty strings to avoid overlap
y_labels = ['' if i % step_size != 0 else str(k) for i, k in enumerate(sorted_correct_cwe_counts.keys())]

# Plotting the horizontal bar chart with adjustments
bar_height = 1  # Set bar height to 1 to make bars adjacent
plt.barh(range(len(sorted_correct_cwe_counts)), list(sorted_correct_cwe_counts.values()), height=bar_height,
         color='gray', edgecolor='black')  # Set bar color to gray and border to black

# Adding title and labels with a smaller font size
plt.title('Distribution of Correctly Predicted Vulnerabilities Across CWE Categories', fontsize=16)
plt.xlabel('Number of Correct Predictions', fontsize=14)

# Set the y-ticks and labels
plt.yticks(y_ticks, [y_labels[i] for i in y_ticks], fontsize=ytick_font_size)

# Additional adjustments
plt.grid(axis='x', linestyle='--', linewidth=0.7)
plt.tight_layout()

# Show the plot
plt.savefig('draw67.png', format='png', dpi=300)  # Save as PNG with high resolution
plt.show()
