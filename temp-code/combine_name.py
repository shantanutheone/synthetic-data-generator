import csv

def format_name(name):
    return name.capitalize()

def match_names(last_name_file, name_file, output_file):
    matched_names = []

    with open(last_name_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        last_names = [row[0].strip().title() for row in reader]
    print(last_names[:10])
    with open(name_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader) 
        names = [row[0].strip() for row in reader]
    print(names[:10])
    for last_name, name in zip(last_names, names):
        first_name, last_name = name, last_name
        matched_names.append(f"{first_name} {last_name}")

    # Write matched names to output CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Full Name'])
        writer.writerows([[name] for name in matched_names])

if __name__ == "__main__":
    last_name_file = "database/intersurnames.csv"
    name_file = "database/name-general.csv"
    output_file = "matched_names.csv"

    match_names(last_name_file, name_file, output_file)

    print("Names matched and written to 'matched_names.csv' successfully.")
