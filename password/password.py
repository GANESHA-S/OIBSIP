import random
import string

def generate_password(length, letters, numbers, symbols):

    char_pool = ""
    if letters:
        char_pool += string.ascii_letters
    if numbers:
        char_pool += string.digits 
    if symbols:
        char_pool += string.punctuation  

    if not char_pool:
        print("Please select atleast one character type.")
        return None

    return ''.join(random.choice(char_pool) for _ in range(length))

def main():
    print("Welcome to the Password Generator!")
    try:
        length = int(input("Enter the desired password length (minimum 4): "))
        if length < 4:
            print("The Password length should be at least of 4 characters.")
            return

        letters = input("Should the password include letters? (yes/no): ").strip().lower() in ['yes', 'y']
        numbers = input("Should the password include numbers? (yes/no): ").strip().lower() in ['yes', 'y']
        symbols = input("Should the password include symbols? (yes/no): ").strip().lower() in ['yes', 'y']

        password = generate_password(length, letters, numbers, symbols)
        if password:
            print(f"Your generated password is: {password}")
    except ValueError:
        print("Error: Please enter a valid number for the password length.")

if __name__ == "__main__":
    main()
