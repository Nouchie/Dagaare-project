import pandas as pd
import csv
import unicodedata

# Open the CSV file
with open("csv_file_created.csv", newline='', encoding='utf-8') as csvfile:
    # Create a CSV reader
    reader = csv.reader(csvfile)
    
    # Iterate over each row in the CSV file
    for row in reader:
        print(row)  # Print each row to inspect the data

# Step 1: Load the CSV file into a DataFrame
df = pd.read_csv("csv_file_created.csv")

# Step 2: Preprocess the data

# Remove rows with missing values
df.dropna(inplace=True)

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# Clean up the text data (e.g., remove unnecessary characters, lowercase everything)
def clean_text(text):
    # Encode the text to UTF-8 to handle special characters
    text = text.encode('utf-8', 'ignore').decode('utf-8')
    # Example cleaning steps: remove extra spaces and convert to lowercase
    return " ".join(text.split()).lower()

# Apply the cleaning function to relevant columns
columns_to_clean = ['word', 'pronunciation', 'word_type', 'definitions', 'examples', 'pl']
for col in columns_to_clean:
    df[col] = df[col].apply(clean_text)

# Print the preprocessed DataFrame to inspect the changes
print("Preprocessed DataFrame:")
print(df)

# Step 3: Save the preprocessed data back to a CSV file
df.to_csv("preprocessed_data.csv", index=False, encoding='utf-8-sig')

print("Preprocessing complete. Preprocessed data saved to preprocessed_data.csv.")
