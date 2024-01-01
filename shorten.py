import csv
import os

# Specify the input file path
input_file_path = 'data\\release_train_patients\\release_train_patients.csv'

# Create an output directory if it doesn't exist
output_directory = 'output'
os.makedirs(output_directory, exist_ok=True)

# Open the input CSV file for reading
with open(input_file_path, 'r', newline='', encoding='utf-8') as input_file:
    # Create a CSV reader object
    csv_reader = csv.reader(input_file)

    # Read the header (assuming the input file has a header)
    header = next(csv_reader)

    for file_number in range(5):
        # Specify the output file path for each block
        output_file_path = os.path.join(output_directory, f'output_{file_number + 1}.csv')

        # Open the output CSV file for writing
        with open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
            # Create a CSV writer object
            csv_writer = csv.writer(output_file)

            # Write the header to each output file
            csv_writer.writerow(header)

            # Write the next 30,000 lines to the output file
            for i, row in enumerate(csv_reader):
                if i < 30000:
                    csv_writer.writerow(row)
                else:
                    break

print("Extraction completed. First 30,000 lines written to", output_file_path)
