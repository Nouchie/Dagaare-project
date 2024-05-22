"""import csv

def extract_words_and_definitions(csv_filename):
    word = []

    with open(csv_filename, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            try:
                if row:
                    definition = row.get('Word', '').strip()
                    if definition:
                        word.append(definition)
            except AttributeError as e:
                print(f"Error processing row: {row} - {e}")
    
    return word

def save_to_csv(data, output_filename):
    with open(output_filename, mode='w', encoding='utf-8', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Word"])  # Write header
        for word in data:
            csv_writer.writerow([word])

if __name__ == "__main__":
    input_filename = 'combined_dictionary.csv'
    output_filename = 'dagaare_words_sentences.txt'
    
    word = extract_words_and_definitions(input_filename)
    save_to_csv(word, output_filename)
    
    print(f"Extracted {len(word)} definitions to {output_filename}")"""

"""
import csv

def find_words_without_definition(csv_filename):
    words_without_definition = []

    with open(csv_filename, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            word = row.get('Word', '').strip()
            definition = row.get('Definition', '').strip()
            if not definition:
                words_without_definition.append(word)

    return words_without_definition

if __name__ == "__main__":
    input_filename = 'combined_dictionary.csv'
    
    words_without_definition = find_words_without_definition(input_filename)
    
    if words_without_definition:
        print("Words without definition:")
        for word in words_without_definition:
            print(word)
    else:
        print("All words have definitions.")
"""

def extract_letters_from_file(input_filename):
    letters = set()  # Using a set to avoid duplicate letters

    with open(input_filename, mode='r', encoding='utf-8') as file:
        for line in file:
            for char in line.strip():
                if char.isalpha():  # Check if the character is a letter
                    letters.add(char)

    return sorted(letters)  # Return letters sorted alphabetically

def save_letters_to_file(letters, output_filename):
    with open(output_filename, mode='w', encoding='utf-8') as file:
        for letter in letters:
            file.write(letter + '\n')

if __name__ == "__main__":
    input_filename = 'dagaare_definition_sentences.txt'
    output_filename = 'dagaare_letters2.txt'
    
    letters = extract_letters_from_file(input_filename)
    save_letters_to_file(letters, output_filename)
    
    print(f"Extracted {len(letters)} unique letters to {output_filename}")


"""def count_characters_in_file(input_filename):
    total_characters = 0

    with open(input_filename, mode='r', encoding='utf-8') as file:
        for line in file:
            total_characters += len(line)
    
    return total_characters

if __name__ == "__main__":
    input_filename = 'dagaare_definition_sentences.txt'
    
    total_characters = count_characters_in_file(input_filename)
    
    print(f"The total number of characters in the file '{input_filename}' is {total_characters}")"""
