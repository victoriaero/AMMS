import os
import csv

# Define the directory path containing the CSV files
directory_path = "/home/yanaquino/Desktop/disc/meu/tp2/commencao/semdup/semcol3/unique"

# Define the specific CSV file to compare against
specific_file_path = "/home/yanaquino/Desktop/disc/meu/botids.txt"

# Create a set to store unique values from the specific file
unique_values = set()

# Read the specific file and store its first column values
with open(specific_file_path, "r", newline="") as specific_file:
    csv_reader = csv.reader(specific_file)
    for row in csv_reader:
        if row:  # Ensure the row is not empty
            unique_values.add(row[0])

# Process each CSV file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith(".csv"):
        input_file_path = os.path.join(directory_path, filename)
        output_file_path = os.path.join(directory_path, "sembots_" + filename)

        with open(input_file_path, "r", newline="") as input_file:
            with open(output_file_path, "w", newline="") as output_file:
                csv_reader = csv.reader(input_file)
                csv_writer = csv.writer(output_file)

                for row in csv_reader:
                    if row and row[0] not in unique_values:
                        csv_writer.writerow(row)

        print(f"Processed {filename} and saved to {output_file_path}")

print("All files in the directory have been processed.")
