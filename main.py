import pymysql
import os
import sys
import random as r
import string as s
import pickle

def choose_user():
    print("\nBucket List Manager")
    print("\nAre you a new user or an existing user?")
    print("1 for New User")
    print("2 for Existing User")
    return int(input("Type: "))

def display_menu():
    print("1. Add Item to Bucket List")
    print("2. View Bucket List")
    print("3. Mark Item as Completed")
    print("4. Exit")
    print("5. Restart")
    return int(input("Type: "))

def generate_random_digits():
    rand_digits = s.digits
    digits = ""
    for i in range(7): 
        y = r.choice(rand_digits)
        digits +=y

# Function to restart the program
def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

# CONNECTING MYSQL
def check_user_exists(new_password):
    db_config = {
        "host": "localhost",
        "user": "Vidha",
        "password": "Vidha@1234",
        "database": "user_passwords_bucket_list",
    }

    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    check_user_query = "SELECT bucketlist_name FROM user_passwords_bucket_list WHERE passwords = %s"
    cursor.execute(check_user_query, (new_password,))
    results = cursor.fetchall()

    # Closing the connection
    connection.close()

    return results

def pass_in_db(new_password):
    existing_buckets = check_user_exists(new_password)
    
    if existing_buckets:
        print("The password already exists. Choose a new one.")
        print("Existing bucket list names:", ', '.join(bucket[0] for bucket in existing_buckets))
        restart_program()
    else:
        digits = generate_random_digits()
        bucket_list_name = "bucketlist" + digits

        db_config = {
            "host": "localhost",
            "user": "Vidha",
            "password": "Vidha@1234",
            "database": "user_passwords_bucket_list",
        }

        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        insert_data_query = "INSERT INTO user_passwords_bucket_list (passwords, bucketlist_name) VALUES (%s, %s)"
        cursor.execute(insert_data_query, (new_password, bucket_list_name))

        connection.commit()
        connection.close()

        print(f"Welcome! Your bucket list name is {bucket_list_name}.")
        return bucket_list_name

def save_bucket_list(bucket_list_name, bucket_list):
    with open(f"{bucket_list_name}.bin", "wb") as file:
        pickle.dump(bucket_list, file)

def load_bucket_list(bucket_list_name):
    try:
        with open(f"{bucket_list_name}.bin", "rb") as file:
            return pickle.load(file)
    except (FileNotFoundError, EOFError):
        return []

if __name__ == "__main__":
    user = choose_user()

    if user == 1:
        print("Let's make an account for you.")
        new_pass = input("Type in your password: ")
        bucket_list_name = pass_in_db(new_pass)
    else:
        while True:
            choice = display_menu()

            if choice == 1:
                # Add Item to Bucket List
                bucket_list_name = input("Enter your bucket list name: ")
                bucket_list = load_bucket_list(bucket_list_name)
                new_item = input("Enter the item for your bucket list: ")
                bucket_list.append(new_item)
                save_bucket_list(bucket_list_name, bucket_list)
                print("Item added to your bucket list!")
            elif choice == 2:
                # View Bucket List
                bucket_list_name = input("Enter your bucket list name: ")
                bucket_list = load_bucket_list(bucket_list_name)
                print("\nBucket List:")
                if not bucket_list:
                    print("Your bucket list is empty.")
                else:
                    for i, item in enumerate(bucket_list, 1):
                        print(f"{i}. {item}")
            elif choice == 3:
                # Mark Item as Completed
                bucket_list_name = input("Enter your bucket list name: ")
                bucket_list = load_bucket_list(bucket_list_name)
                print("\nBucket List:")
                if not bucket_list:
                    print("Your bucket list is empty.")
                else:
                    for i, item in enumerate(bucket_list, 1):
                        print(f"{i}. {item}")

                try:
                    item_number = int(input("Enter the item number to mark as completed: "))
                    if 1 <= item_number <= len(bucket_list):
                        bucket_list[item_number - 1] = "[Completed] " + bucket_list[item_number - 1]
                        save_bucket_list(bucket_list_name, bucket_list)
                        print("Item marked as completed.")
                    else:
                        print("Invalid item number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            elif choice == 4:
                print("Exiting Bucket List Manager. Goodbye!")
                break
            elif choice == 5:
                print("Restarting")
                restart_program()
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

