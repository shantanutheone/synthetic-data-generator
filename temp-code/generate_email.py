import csv
import random
import string
import unicodedata

def remove_special_chars(name):
    return ''.join(c for c in unicodedata.normalize('NFKD', name) if not unicodedata.combining(c))

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

def generate_email(name, domains):
    name = remove_special_chars(name.lower().replace(" ", ""))  
    email = name + generate_random_string(4)  
    domain = random.choice(domains)
    return f"{email}@{domain}"

def generate_emails(input_file, output_file, domains):
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        names = [row[0] for row in reader]

    name_emails = []
    for name in names:
        email = generate_email(name, domains)
        name_emails.append([name, email])

    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Email'])
        writer.writerows(name_emails)

if __name__ == "__main__":
    input_file = "database/name-general.csv"
    output_file = "generated_emails.csv"
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"] 

    generate_emails(input_file, output_file, domains)

    print("Emails generated and written to 'generated_emails.csv' successfully.")