import csv
from collections import OrderedDict

# Define paths
csv_file_created_path = "csv_file_created.csv"
examples_with_brackets_path = "examples_with_brackets.csv"

# Read data from examples_with_brackets.csv
new_data = []
with open(examples_with_brackets_path, 'r', newline='', encoding='utf-8') as input_file:
    reader = csv.DictReader(input_file)
    for row in reader:
        new_data.append(OrderedDict(row))  # Preserve order

# Read existing data from csv_file_created.csv and remove duplicates
existing_data = []
with open(csv_file_created_path, 'r', newline='', encoding='utf-8') as input_file:
    reader = csv.DictReader(input_file)
    existing_data = [row for row in reader]

# Remove duplicates from existing data
existing_data_ids = set()
unique_existing_data = []
for row in existing_data:
    # Check if 'type' exists in the row
    if 'type' in row:
        row_id = (row.get('word', ''), row.get('pronunciation', ''), row.get('type', ''), row.get('definitions', ''))
    else:
        # Handle case where 'type' is missing
        row_id = (row.get('word', ''), row.get('pronunciation', ''), '', row.get('definitions', ''))
    
    if row_id not in existing_data_ids:
        unique_existing_data.append(row)
        existing_data_ids.add(row_id)


# Merge new data with unique existing data
merged_data = unique_existing_data + new_data

# Write merged data back to csv_file_created.csv
with open(csv_file_created_path, 'w', newline='', encoding='utf-8') as output_file:
    fieldnames = ['word', 'pronunciation', 'type', 'definitions', 'examples', 'pl']
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(merged_data)

print("Merged data saved to csv_file_created.csv.")
