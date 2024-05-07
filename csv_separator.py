import csv

def clean_filename(filename):
    # Replace problematic symbols with underscores
    cleaned_filename = filename.replace('/', '').replace('|', '').replace(',', '').replace('"', '').replace('<', '').replace('>', '').replace(' ', '_')
    return cleaned_filename

def split_csv(csv_file):
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            apartment_name = row['Apartment Name']
            filename = f"barcelona_splitted_csv/{clean_filename(apartment_name)}.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
                writer.writeheader()
                writer.writerow(row)
            print(f"File '{filename}' has been created.")

# Replace 'your_file.csv' with the path to your CSV file
split_csv('barcelona.csv')