import os
import csv

def extract_valid_rows(csv_file, output_file, max_records_per_file=1000, max_total_records=10000, encoding='utf-8'):
    required_columns = ['LON', 'LAT', 'STREET', 'CITY', 'DISTRICT', 'REGION', 'POSTCODE']
    records_written = 0
    with open(csv_file, 'r', encoding=encoding) as file:
        reader = csv.DictReader(file)
        valid_rows = []
        for row in reader:
            null_count = sum(1 for col in required_columns if row.get(col) == '' or row.get(col) is None)
            if null_count <= 1:
                valid_row = {col: row[col] for col in required_columns}
                valid_rows.append(valid_row)
                records_written += 1
                if records_written >= max_records_per_file or records_written >= max_total_records:
                    break

    if valid_rows:
        with open(output_file, 'a', newline='', encoding=encoding) as out_file:
            writer = csv.DictWriter(out_file, fieldnames=required_columns)
            if out_file.tell() == 0:
                writer.writeheader()
            writer.writerows(valid_rows)

        return records_written
    else:
        return 0

def list_csv_files(folder_path):
    csv_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(os.path.join(root, file))
    return csv_files

def main(folder_path, output_file, max_total_records=10000, max_records_per_file=1000):
    csv_files = list_csv_files(folder_path)
    total_records_written = 0
    for csv_file in csv_files:
        records_written = extract_valid_rows(csv_file, output_file, max_records_per_file, max_total_records - total_records_written)
        total_records_written += records_written
        if total_records_written >= max_total_records:
            break


folder_path = "database/openaddr-collected-asia"
output_file = "output.csv"
max_records = 10000
main(folder_path, output_file, max_records)
