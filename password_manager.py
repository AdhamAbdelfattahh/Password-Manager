import os
import json
from cryptography.fernet import Fernet
import getpass
import random
import string

# Function to generate a secure password
def generate_password(length=12, use_special_chars=True):
    characters = string.ascii_letters + string.digits
    if use_special_chars:
        characters += string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Function to load the encryption key
def load_key():
    return open("secret.key", "rb").read()

# Function to save a new password
def save_password(service, password):
    key = load_key()
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    if os.path.exists('passwords.json'):
        with open('passwords.json', 'r') as file:
            data = json.load(file)
    else:
        data = {}
    data[service] = encrypted_password.decode()
    with open('passwords.json', 'w') as file:
        json.dump(data, file)

# Function to retrieve a password
def retrieve_password(service):
    key = load_key()
    fernet = Fernet(key)
    with open('passwords.json', 'r') as file:
        data = json.load(file)
    encrypted_password = data.get(service)
    if encrypted_password:
        return fernet.decrypt(encrypted_password.encode()).decode()
    else:
        return None

# Generate and save the encryption key
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Main program
if __name__ == "__main__":
    if not os.path.exists("secret.key"):
        generate_key()

    while True:
        action = input("Do you want to (s)ave a password, (r)etrieve a password, or (g)enerate a password? (q to quit): ").lower()
        if action == 's':
            service = input("Enter the name of the service: ")
            password = input("Enter the password (or leave empty to generate one): ")
            if not password:
                password = generate_password()
                print(f"Generated Password: {password}")
            save_password(service, password)
            print("Password saved successfully.")
        elif action == 'r':
            service = input("Enter the name of the service: ")
            password = retrieve_password(service)
            if password:
                print(f"Password for {service}: {password}")
            else:
                print("No password found for that service.")
        elif action == 'g':
            length = int(input("Enter the desired password length: "))
            use_special = input("Include special characters? (y/n): ").lower() == 'y'
            new_password = generate_password(length, use_special)
            print(f"Generated Password: {new_password}")
        elif action == 'q':
            break
        else:
            print("Invalid option. Please try again.")
