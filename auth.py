import csv
import os


FILE_NAME = "users.csv"


# ============================================================
# Create users.csv if it doesn't exist
# ============================================================

def initialize_users_file():

    if not os.path.exists(FILE_NAME):

        with open(FILE_NAME, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Name",
                "Email",
                "Username",
                "Password"
            ])


# ============================================================
# Register New User
# ============================================================

def register_user(name, email, username, password):

    initialize_users_file()

    with open(FILE_NAME, "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["Username"].lower() == username.lower():

                return False

    with open(FILE_NAME, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            name,
            email,
            username,
            password
        ])

    return True


# ============================================================
# Login Verification
# ============================================================

def login_user(username, password):

    initialize_users_file()

    with open(FILE_NAME, "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            if (
                row["Username"] == username and
                row["Password"] == password
            ):

                return True

    return False