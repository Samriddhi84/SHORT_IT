import json
import datetime

# Sample JSON data
with open("users.json", "r") as file:
    data = file.read()


# Load the JSON data into a Python dictionary
user_data = json.loads(data)

# CRUD Operations


def save_data(user_data=None) -> None:
    if user_data is None:
        user_data = user_data
    with open("users.json", "w") as file:
        json.dump(user_data, file)
        # data=file.read()
        # user_data = json.loads(data)


# Create or Update User
def save_user(email, name, password):
    password = hash_password(password)
    user_data[email] = {
        "name": name,
        "email": email,
        "plaintext_password": password,
        "urls": {},
    }
    save_data()
    return True, f"User '{email}' saved."


# Read User
def get_user(email):
    user = user_data.get(email)
    if user:
        return True, user
    return False, "User not found."


# Update User
def update_user(email, name=None, password=None):
    user = user_data.get(email)
    if user:
        if name:
            user["name"] = name
        if password:
            user["plaintext_password"] = hash_password(password)
        save_data()
        return True, f"User '{email}' updated."
    else:
        save_data()
        return False, "User not found."


# Delete User
def delete_user(email):
    if email in user_data:
        del user_data[email]
        save_data()
        return True, f"User '{email}' deleted."
    else:
        save_data()
        return False, "User not found."


# CRUD for URLs


# Create or Update URL Alias
def save_url(email, alias, url):
    exists, _ = get_url(alias)
    print(exists, _)
    if exists:
        return False, "Alias already exists."

    user = user_data.get(email)
    if user:
        user["urls"][alias] = {
            "url": url,
            "created_at": datetime.datetime.now().isoformat() + "Z",
            "visits": 0,
        }
        save_data()
        user_data[email] = user
        print(user_data)
        return True, f"Alias '{alias}' saved for user '{email}'."
    else:
        return False, "User not found."


# Read URL Alias
def get_url(alias):
    for user in user_data.values():
        if alias in user["urls"]:
            # save_data()
            return True, user["urls"][alias]
    return False, "Alias not found."


# Update URL Alias
def update_url(email, alias, url):
    user = user_data.get(email)
    if user and alias in user["urls"]:
        user["urls"][alias]["url"] = url
        save_data()
        return True, f"Alias '{alias}' updated for user '{email}'."
    else:
        save_data()
        return False, "Alias not found."


# Delete URL Alias
def delete_url(email, alias):
    user = user_data.get(email)
    if user and alias in user["urls"]:
        del user["urls"][alias]
        save_data()
        return True, f"Alias '{alias}' deleted for user '{email}'."
    else:
        save_data()
        return False, "Alias not found."


def validate_password(email, password):
    user = user_data.get(email)
    if user:
        plaintext_password = user["plaintext_password"]
        return password == plaintext_password
    return False


# Utility Functions
def hash_password(password):
    """Hash the password with bcrypt."""
    return password


# Create random alias based on existing aliases
import random
import string


def create_alias(url):

    alias = url.split("/")[-1]
    randomized_string = "".join(
        random.choices(string.ascii_letters + string.digits, k=6)
    )
    alias = "".join([c for c in alias if c.isalnum()]) or randomized_string
    alias = alias.lower()

    while True:
        if alias not in user_data:
            return alias
        alias += random.choice(string.digits)
