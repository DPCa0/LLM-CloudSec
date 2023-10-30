import pandas as pd

# Load the sampled_vulnerable_codes.csv file and extract CWE IDs
sampled_df = pd.read_csv('sampled_vulnerable_codes.csv')
unique_cwe_from_sampled = sampled_df['CWE'].unique()
id_list = [cwe.replace('CWE', '') for cwe in unique_cwe_from_sampled]

# Manually parse the 888.csv file to extract rows with CWE-IDs
with open('888.csv', 'r') as file:
    lines = file.readlines()

# Extract the first row (headers) and rows with CWE-IDs from the list
header = lines[0]
matched_rows = [header] + [line for line in lines if line.split(',')[0].replace('"', '').strip() in id_list]

# Find the missing CWE-IDs based on the manually parsed file
cwe_ids_from_file = [line.split(',')[0].replace('"', '').strip() for line in matched_rows[1:]]  # Exclude header
missing_cwe_ids = set(id_list) - set(cwe_ids_from_file)

# Save the matched rows to a new CSV file
with open('matched_cwe_data.csv', 'w') as file:
    file.writelines(matched_rows)

print(f"Total CWE-IDs: {len(id_list)}")
print(f"Matched CWE-IDs: {len(cwe_ids_from_file)}")
print(f"Missing CWE-IDs: {missing_cwe_ids}")
