import csv
import json

# def get_description(cwe_id, file_path):
#     with open(file_path, 'r', encoding='utf-8') as csvfile:
#         # Initializing the CSV reader
#         reader = csv.reader(csvfile)
#
#         # Getting the header
#         header = next(reader)
#
#         # Checking if 'CWE-ID', 'Description' and 'Extended Description' columns exist in the header
#         if 'CWE-ID' not in header or 'Description' not in header or 'Extended Description' not in header:
#             raise ValueError("CSV doesn't have the necessary columns")
#
#         # Iterating over rows to find the given CWE-ID
#         for row in reader:
#             if row[header.index('CWE-ID')] == str(cwe_id):
#                 return row[header.index('Description')], row[header.index('Extended Description')]
#
#     return None, None
#
#
# # Path to the CSV file
# file_path = 'dataset/matched_cwe_data.csv'
#
# # Using the function
# cwe_id = 690
# description, extended_description = get_description(cwe_id, file_path)
# if description and extended_description:
#     print(f"CWE-ID: {cwe_id}")
#     print(f"Description: {description}")
#     print(f"Extended Description: {extended_description}")
# else:
#     print(f"No data found for CWE-ID: {cwe_id}")

with open('test_D2A_cache.json') as f:
    data = json.load(f)
    print(f"数据样例：{data[0]}")
    print(f"总数据量：{len(data)}")
