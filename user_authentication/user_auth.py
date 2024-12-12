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
    def register_user(self):
        common.clear_console()
        common.print_main_header()  # Fixed main header for all the time
        common.print_sub_header("New User Register")

        # Collect user inputs
        username = common.get_valid_username(self)
        full_name = input("Enter your full name: ").strip()
        email = common.get_valid_email(self)
        phone = common.get_valid_phone(self)
        address = input("Enter your address: ").strip()
        password = input("Enter your password: ").strip()

        # Check if username already exists
        if username in self.users:
            return common.color_text("Error: Username already exists.", "red")

        # Add user information to the dictionary
        self.users[username] = {
            "username": username,
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "address": address,
            "password": self.hash_password(password),  # Store hashed password
            "role": "customer"  # Default role
        }

        # Save users and return success message
        self.save_users()
        return common.color_text(f"User {username.title()} registered successfully.", "green")




    # Login a user
    def login_user(self):
        common.clear_console()
        common.print_main_header()  # Fixed main header for all the time
        common.print_sub_header("User Login Form")

        username = input("Username: ").strip()
        password = input("Password: ").strip()

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
        return common.color_text(f" Welcome back {username.title()}! ", color="green", style="bold", bg_color="blue")
  

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
        return common.color_text(f"You have successfully logged out", "green")

    
    # Method to hash a password
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    # View all users (Admin only)
    def view_all_users(self):
        common.clear_console()
        common.print_main_header()  # Fixed main header for all the time
        common.print_sub_header("View All Users")

        if not self.has_role("admin"):
            return common.color_text("Permission denied. Only admins can view all users.", color="red", style="bold")

        if not self.users:
            return common.color_text("No users found in the system.", color="yellow", style="italic")

        username_width = 20
        role_width = 20
        email_width = 35

        # Header with blue background
        header = common.color_text(f"{' Username':<{username_width}}{'Role':<{role_width}}{'Email':<{email_width}}", bg_color="blue", style="bold")
        
        # Create separator line
        separator = "-" * 75

        # Format each user row to match the fixed column widths
        rows = "\n".join(
            f"{user['username']:<{username_width}}{user['role']:<{role_width}}{user['email']:<{email_width}}"
            for user in self.users.values()
        )

        # Return the complete formatted string with sub-header as title
        return f"{header}\n{separator}\n{rows}"
    

    # Search a user by username, email, phone or full name (Admin only)
    def search_user(self):
        user_search_key = input("Search by username, email, phone or full name: ")
        common.clear_console()
        common.print_main_header()
        common.print_sub_header("Search Users")

        if not self.has_role("admin"):
            return common.color_text("Permission denied. Only admins can search for users.", color="red", style="bold")

        results = [
            user for user in self.users.values()
            if user_search_key.lower() in user["username"].lower()
            or user_search_key.lower() in user["email"].lower()
            or user_search_key.lower() in user["full_name"].lower()
            or user_search_key in user["phone"]
        ]

        if not results:
            return common.color_text(f"No users found matching '{user_search_key}'.", color="yellow")

        username_width = 20
        role_width = 20
        email_width = 35

        # Header with blue background
        header = common.color_text(f"{' Username':<{username_width}}{'Role':<{role_width}}{'Email':<{email_width}}", bg_color="blue", style="bold")
        
        # Create separator line
        separator = "-" * 75

        # Format each user row to match the fixed column widths
        rows = "\n".join(
            f"{user['username']:<{username_width}}{user['role']:<{role_width}}{user['email']:<{email_width}}"
            for user in results
        )

        return f"{header}\n{separator}\n{rows}"

    # Update user role (Admin only)
    def update_role(self, admin_username, target_username, new_role):
        common.clear_console()
        common.print_main_header()
        common.print_sub_header("Update User Role")

        if not self.has_role("admin") or self.session.get("username") != admin_username:
            return common.color_text("Permission denied. Only admins can update roles.", color="red", style="bold")

        if target_username not in self.users:
            return common.color_text("Target user does not exist.", color="yellow")

        self.users[target_username]["role"] = new_role
        self.save_users()
        return common.color_text(f"Updated {target_username}'s role to {new_role}.", color="green", style="bold")

    # View all workers (Admin only)
    def view_all_workers(self):
        common.clear_console()
        common.print_main_header()
        common.print_sub_header("View All Workers")

        if not self.has_role("admin"):
            return common.color_text("Permission denied. Only admins can view workers.", color="red", style="bold")

        workers = [
            user for user in self.users.values() if user["role"] in ["manager", "staff"]
        ]

        if not workers:
            return common.color_text("No workers (managers or staff) found in the system.", color="yellow", style="italic")

        username_width = 20
        full_name_width = 25
        email_width = 35
        role_width = 15

        # Header with blue background
        header = common.color_text(f"{' Username':<{username_width}}{'Full Name':<{full_name_width}}{'Email':<{email_width}}{'Role':<{role_width}}", bg_color="blue", style="bold")
        
        # Create separator line
        separator = "-" * 75

        # Format each user row to match the fixed column widths
        rows = "\n".join(
            f"{worker['username']:<{username_width}}{worker['full_name']:<{full_name_width}}{worker['email']:<{email_width}}{worker['role']:<{role_width}}"
            for worker in workers
        )

        return f"{header}\n{separator}\n{rows}"