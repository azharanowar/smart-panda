import json
import utilities.common as common
import hashlib

class UserAuth:
    def __init__(self, users_file="users.json", session_file="session.json"):
        self.users_file = users_file
        self.session_file = session_file
        self.users = self.load_users()
        self.session = self.load_session()

    # Register user
    def register_user(self, username, full_name, email, phone, address, password):
        if username in self.users:
            return "Error: Username already exists."
        
        # Add user information to the dictionary
        self.users[username] = {
            "username": username,  # Ensure username is the key
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "address": address,
            "password": self.hash_password(password),  # Store hashed password
            "role": "customer"  # Default role
        }

        self.save_users()  # Save the updated user list
        return f"User {username} registered successfully."



    # Login a user
    def login_user(self, username, password):
        user = self.users.get(username)
        
        # Error message for username not found
        if not user:
            return common.color_text("Username not found. Enter correct your username!", color="red", style="bold")

        # Error message for incorrect password
        if user["password"] != self.hash_password(password):
            return common.color_text("Incorrect password. Please enter your correct password!", color="red", style="bold")

        # Success message for login
        self.session = {"username": username, "role": user["role"]}
        self.save_session()
        
        # Displaying a success message with green text and background
        return common.color_text(f" Welcome back to the SmartPanda, {username}! ", color="green", style="bold", bg_color="blue")
  

    # Load users from file
    def load_users(self):
        try:
            with open(self.users_file, "r") as file:
                users = json.load(file)
                # Ensure the structure is correct and each user has a 'username'
                for username, user_data in users.items():
                    if 'username' not in user_data:
                        user_data['username'] = username  # Add username key if missing
                return users
        except FileNotFoundError:
            return {}  # Return an empty dictionary if the file doesn't exist
        except json.JSONDecodeError:
            print("Warning: users.json is empty or corrupted. Starting with an empty user database.")
            return {}  # Return an empty dictionary if the file is empty or corrupted



    # Save users to file
    def save_users(self):
        with open(self.users_file, "w") as file:
            json.dump(self.users, file, indent=4)

    # Load session data
    def load_session(self):
        try:
            with open(self.session_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    # Save session data
    def save_session(self):
        with open(self.session_file, "w") as file:
            json.dump(self.session, file, indent=4)

    # Check if a field is unique
    def is_unique(self, field, value):
        # Check if any user has the same field value
        return all(user.get(field) != value for user in self.users.values())
    

    # Check if logged in
    def is_logged_in(self):
        return "username" in self.session

    # Check role
    def has_role(self, role):
        return self.session.get("role") == role

    # Logout user
    def logout_user(self):
        self.session = {}
        self.save_session()
        return "Logged out successfully."

    # Update user role (Admin only)
    def update_role(self, admin_username, target_username, new_role):
        if not self.has_role("admin") or self.session.get("username") != admin_username:
            return "Permission denied. Only admins can update roles."
        if target_username not in self.users:
            return "Target user does not exist."

        self.users[target_username]["role"] = new_role
        self.save_users()
        return f"Updated {target_username}'s role to {new_role}."
    
    # Helper function to hash a password
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
