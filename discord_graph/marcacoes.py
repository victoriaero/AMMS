import os
import re

OUTPUT_DIRECTORY = "mencoes"

# Define a regular expression pattern to match <...> tags with user IDs
pattern = re.compile(r'<@!?&?([^>]+)>')

# Function to process a single file
def process_file(file_path):
    user_info = []

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split(',')
            if len(parts) >= 4 and pattern.search(parts[3]):
                user_id = parts[1]
                username = parts[2]
                message = ' '.join(parts[3:])
                mentions = ' '.join(match.group(1) for match in pattern.finditer(message))

                if mentions:
                    final_message = mentions + '\n'
                    user_info.append((user_id, username, final_message))
    
    return user_info

# Function to process all .txt files in a directory
def process_directory(directory):
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIRECTORY, f"{directory}.txt")

    with open(output_file, 'w') as output:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    user_info = process_file(file_path)
                    for info in user_info:
                        output.write(f"{info[0]}, {info[1]}, {info[2]}")
                    # output.write('\n')

# Process directories and subdirectories
for root, _, _ in os.walk('.'):
    if root.startswith('./'):
        process_directory(root[2:])

print("Processing complete.")
