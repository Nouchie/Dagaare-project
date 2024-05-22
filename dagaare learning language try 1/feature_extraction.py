import re

def extract_features(entry):
    # Initialize features dictionary
    features = {}
    
    # Extract word, type, pronunciation, definitions, and examples (if available)
    word_match = re.search(r'Word:\s*(.*?)\n', entry)
    type_match = re.search(r'Type:\s*(.*?)\n', entry)
    pronunciation_match = re.search(r'Pronunciation:\s*(.*?)\n', entry)
    definitions_match = re.findall(r'Definitions:\s*(.*?)\n(?:(?:[A-Z][a-z]+|Examples):|$)', entry, re.DOTALL)
    examples_match = re.findall(r'Examples:\s*(.*?)\n', entry)
    
    # Extract word length
    if word_match:
        features['word_length'] = len(word_match.group(1))
    else:
        features['word_length'] = 0
    
    # Extract type
    if type_match:
        features['type'] = type_match.group(1)
    else:
        features['type'] = None
    
    # Extract pronunciation length
    if pronunciation_match:
        features['pronunciation_length'] = len(pronunciation_match.group(1))
    else:
        features['pronunciation_length'] = 0
    
    # Extract number of definitions
    features['num_definitions'] = len(definitions_match)
    
    # Extract examples length and presence of examples
    if examples_match:
        examples_text = ' '.join(examples_match)
        features['examples_length'] = len(examples_text)
        features['has_examples'] = True
    else:
        features['examples_length'] = 0
        features['has_examples'] = False
    
    return features

# Open and read the data file
with open("tokenized.txt", "r", encoding="utf-8") as file:
    data = file.read().split("\n\n")  # Split entries by empty lines
    
    # List to store extracted features for each entry
    all_features = []

    # Loop through each entry
    for entry in data:
        features = extract_features(entry)
        all_features.append(features)

# Display the first few entries of extracted features
for i, features in enumerate(all_features[:5], start=1):
    print(f"Entry {i} Features:", features)
