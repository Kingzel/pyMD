import csv
import os

input_file_path = 'data\\release_train_patients\\release_train_patients.csv'

# Create an output directory if it doesn't exist already
output_directory = 'output'
os.makedirs(output_directory, exist_ok=True)

# Open the input CSV file for reading
with open(input_file_path, 'r', newline='', encoding='utf-8') as input_file:
    csv_reader = csv.reader(input_file)

    # Reading the header and storing it
    header = next(csv_reader)

    for file_number in range(5):
        # Specify the output file path for each block
        output_file_path = os.path.join(output_directory, f'output_{file_number + 1}.csv')

        with open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
            csv_writer = csv.writer(output_file)

            # Write the header to each output file
            csv_writer.writerow(header)


            #In blocks of 30000 lines sequentially output 5 files. (150k total)
            for i, row in enumerate(csv_reader):
                if i < 30000:
                    csv_writer.writerow(row)
                else:
                    break

print("Extraction completed.")
