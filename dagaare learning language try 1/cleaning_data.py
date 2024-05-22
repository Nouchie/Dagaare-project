def clean_dictionary(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = []
    current_entry = ''

    for line in lines:
        # Check if the line starts with a word
        if line.strip() and line[0].isalpha():
            # If current entry is not empty, append it to the cleaned lines
            if current_entry:
                cleaned_lines.append(current_entry.strip())
            # Start a new entry
            current_entry = line.strip()
        else:
            # Append the line to the current entry
            current_entry += ' ' + line.strip()

    # Append the last entry
    if current_entry:
        cleaned_lines.append(current_entry.strip())

    # Write the cleaned lines to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in cleaned_lines:
            f.write(line + '\n')

# Provide the paths to your input and output files
input_file_path = 'dagaare.txt'
output_file_path = 'cleaned_dictionary.txt'

# Clean the dictionary data
clean_dictionary(input_file_path, output_file_path)
