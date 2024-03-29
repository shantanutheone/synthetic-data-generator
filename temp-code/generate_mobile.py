import csv
import random

def generate_mobile_number(country_code):
    if country_code == '+1':  # USA format
        mobile_number = country_code + str(random.randint(200, 999)) + '-' + str(random.randint(200, 999)) + '-' + str(random.randint(1000, 9999))
    elif country_code == '+44':  # UK format
        mobile_number = country_code + '7' + ''.join(str(random.randint(0, 9)) for _ in range(9))
    elif country_code == '+91':  # India format
        mobile_number = country_code + '9' + ''.join(str(random.randint(0, 9)) for _ in range(9))
    elif country_code == '+33':  # France format
        mobile_number = country_code + '6' + ''.join(str(random.randint(0, 9)) for _ in range(8))
    elif country_code == '+81':  # Japan format
        mobile_number = country_code + '90-' + ''.join(str(random.randint(0, 9)) for _ in range(8))
    elif country_code == '+61':  # Australia format
        mobile_number = country_code + '4' + ''.join(str(random.randint(0, 9)) for _ in range(8))
    elif country_code == '+86':  # China format
        mobile_number = country_code + '1' + ''.join(str(random.randint(0, 9)) for _ in range(9))
    elif country_code == '+49':  # Germany format
        mobile_number = country_code + '1' + ''.join(str(random.randint(0, 9)) for _ in range(10))
    elif country_code == '+39':  # Italy format
        mobile_number = country_code + '3' + ''.join(str(random.randint(0, 9)) for _ in range(9))
    elif country_code == '+7':  # Russia format
        mobile_number = country_code + '9' + ''.join(str(random.randint(0, 9)) for _ in range(9))
    else:
        raise ValueError("Country code not supported")
    return mobile_number

def write_to_csv(filename, mobile_numbers):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Mobile Number'])
        writer.writerows([[number] for number in mobile_numbers])

if __name__ == "__main__":
    country_codes = ['+1', '+44', '+91', '+33', '+81', '+61', '+86', '+49', '+39', '+7']
    mobile_numbers = [generate_mobile_number(code) for code in country_codes for _ in range(1000)]
    write_to_csv('database/mobile-general.csv', mobile_numbers)
    print("CSV file 'mobile_numbers.csv' generated successfully.")
