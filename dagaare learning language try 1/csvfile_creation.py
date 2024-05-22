import re
import csv

def tokenize_text(text):
    # Initialize variables to store tokenized data
    tokenized_data = []

    # Split text into lines
    lines = text.split('\n')

    # Initialize variables to store current entry data
    word = None
    pronunciation = None
    word_type = None
    definitions = []
    examples = []
    pl = None

    # Process each line
    for line in lines:
        # Extract word
        word_match = re.search(r'(\w+)\s*\[', line)
        if word_match:
            # Save previous entry data if present
            if word:
                entry = {
                    'word': word,
                    'pronunciation': pronunciation,
                    'word_type': word_type,
                    'definitions': ', '.join(definitions),
                    'examples': ', '.join(examples),
                    'pl': pl
                }
                tokenized_data.append(entry)
                # Reset variables
                word = None
                pronunciation = None
                word_type = None
                definitions = []
                examples = []
                pl = None
            
            # Extract word
            word = word_match.group(1).strip()
            # Extract pronunciation
            pronunciation_match = re.search(r'\[(.*?)\]', line)
            if pronunciation_match:
                pronunciation = pronunciation_match.group(1).strip()

            # Extract word type
            type_match = re.search(r'\]\s*(\w+)\.', line)
            if type_match:
                word_type = type_match.group(1).strip()

            # Extract definitions and examples
            definitions_match = re.findall(r'•\s*(.*?)\s*(?=(?:pl:|•|$))', line)
            for definition in definitions_match:
                if ':' in definition:
                    if 'pl:' in definition:
                        pl = definition.strip()
                    else:
                        definitions.append(definition.strip())
                else:
                    examples.append(definition.strip())

    # Add last entry if present
    if word:
        entry = {
            'word': word,
            'pronunciation': pronunciation,
            'word_type': word_type,
            'definitions': ', '.join(definitions),
            'examples': ', '.join(examples),
            'pl': pl
        }
        tokenized_data.append(entry)

    return tokenized_data

# Open and read the data file
with open("dagaare.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Tokenize the text
tokenized_data = tokenize_text(text)

# Define CSV file path
csv_file_path = "tokenized_data_new.csv"

# Define field names for CSV header
field_names = ['word', 'pronunciation', 'word_type', 'definitions', 'examples', 'pl']

# Write the tokenized data to a CSV file
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=field_names)

    # Write header
    writer.writeheader()

    # Write each entry's data to the CSV file
    for entry in tokenized_data:
        writer.writerow(entry)

print("Tokenized data saved to tokenized_data.csv.")
