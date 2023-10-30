import pandas as pd

# Load the CSV into a DataFrame
df = pd.read_csv('results/unique_datasets/Juliet.csv')

# Filter out rows where Vulnerable is not 1
vulnerable_df = df[df['Vulnerable'] == 1]

# Extract the CWE number from the ID column using .loc
vulnerable_df.loc[:, 'CWE'] = vulnerable_df['ID'].str.extract('(CWE\d+)')

# Calculate the count of samples for each CWE category
cwe_counts = vulnerable_df['CWE'].value_counts()

# Filter CWE categories that have at least 10 samples
valid_cwe = cwe_counts[cwe_counts >= 10].index
filtered_df = vulnerable_df[vulnerable_df['CWE'].isin(valid_cwe)]

# Group by CWE and take 10 samples from each valid group
sampled_df = filtered_df.groupby('CWE').apply(lambda x: x.sample(10)).reset_index(drop=True)

# Save the sampled data to a new CSV file
sampled_df.to_csv('dataset/sampled_vulnerable_codes.csv', index=False)
