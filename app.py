import utilities.common as common
import user_authentication.user_auth as user_auth

auth = user_auth.UserAuth()
def show_logged_in_menu():
    """Show options based on user role."""
    common.clear_console()

    common.print_main_header()  # Fixed main header for all the time
    if auth.is_logged_in():
        # Display loading animation before final content
        common.loading_message_with_delay("Loading your dashboard", 'green', 2)
        common.clear_console()

        common.print_main_header()  # Fixed main header for all the time
        
        if auth.session["role"] == "admin" or auth.session["role"] == "manager" or auth.session["role"] == "staff":
            common.print_sub_header(f"{auth.session['role'].capitalize()} Dashboard")
            print("1. Manage Inventory")
            print("2. Manage Orders")
            print("3. Manage Users (Only Admin Access)")
            print("4. Logout")

            while True:
                choice = common.get_valid_number_input("Choose an option: ")
                if choice == 1:
                    print("Managing Inventory...")
                elif choice == 2:
                    print("Managing Order...")
                elif choice == 3:
                    print("Managing Users...")
                elif choice == 4:
                    auth.logout_user()
                    show_logged_in_menu()
                else:
                    print(common.color_text("Invalid input choice. Please enter 1, 2, 3, or 4 as valid menu number.", "red"))
                    continue
        else:
            # Customer Dashboard
            common.print_sub_header("Customer Dashboard")
            print("1. New Order")
            print("2. View Orders")
            print("3. Update Order")
            print("4. Cancel Order")
            print("5. Logout")
            while True:
                choice = common.get_valid_number_input("Choose an option: ")
                if choice == 1:
                    print("New Order...")
                elif choice == 2:
                    print("View Orders...")
                elif choice == 3:
                    print("Update Order...")
                elif choice == 4:
                    print("Cancel Order...")
                elif choice == 5:
                    auth.logout_user()
                    show_logged_in_menu()
                else:
                    print(common.color_text("Invalid input choice. Please enter 1, 2, 3, 4 or 5 as valid menu number.", "red"))
                    continue
    else:
        # Non-logged-in options
        common.print_sub_header("User Authentication System")
        print("1. Register")
        print("2. Login")
        while True:
                choice = common.get_valid_number_input("Choose an option: ")
                if choice == 1:
                    common.clear_console()
                    common.loading_message_with_delay("Register form is loading, please wait", 'green', 2)
                    auth.register_user()
                elif choice == 2:
                    common.clear_console()
                    common.loading_message_with_delay("Login form is loading, please wait", 'green', 2)
                    auth.login_user()
                else:
                    print(common.color_text("Invalid input choice. Please enter 1 or 2 as valid menu number.", "red"))
                    continue

def main():
    show_logged_in_menu()  # Display role-based menu
    while False:
        show_logged_in_menu(auth)  # Display role-based menu
        
        if auth.is_logged_in() and (auth.session["role"] == "admin" or auth.session["role"] == "manager" or auth.session["role"] == "staff"):
            # Provide options for logged-in users
            choice = common.get_valid_input("Choose an option: ", valid_options=["1", "2", "3", "4"])
        elif auth.is_logged_in() and auth.session["role"] == "customer":
            # Provide options for logged-in users
            choice = common.get_valid_input("Choose an option: ", valid_options=["1", "2", "3", "4", "5"])
        else:
            # Provide options for non-logged-in users
            choice = common.get_valid_input("Choose an option: ", valid_options=["1", "2", "3"])

        if choice == "1":  # Register, Admin Dashboard, or View Reports/Tasks
            if not auth.is_logged_in():
                # Register a new user
                common.clear_console()
                print(common.color_text("Register New User", "cyan"))
                username = common.get_valid_username(auth)
                full_name = input("Enter your full name: ").strip()
                email = common.get_valid_email(auth)
                phone = common.get_valid_phone(auth)
                address = input("Enter your address: ").strip()
                password = input("Enter your password: ").strip()

                result = auth.register_user(username, full_name, email, phone, address, password)
                common.show_message_with_delay(result, "green")
            else:
                # Role-based options for admin, manager, and staff
                if auth.session["role"] == "admin":
                    # Admin actions like managing users and roles
                    common.show_message_with_delay("Admin: Manage Users and Roles", "cyan")
                    # Implement actions for managing users and roles here
                elif auth.session["role"] == "manager" or auth.session["role"] == "staff":
                    # Manager/Staff actions (same for both)
                    common.show_message_with_delay(f"{auth.session['role'].capitalize()}: View Reports or Manage Tasks", "cyan")
                    # Implement actions for viewing reports or managing tasks here
                else:
                    # Customer actions
                    common.show_message_with_delay("Customer: View Orders or Update Profile", "cyan")
                    # Implement actions for viewing orders or updating profile here
        
        elif choice == "2":  # Login or Logout options
            if not auth.is_logged_in():
                # Login action
                common.clear_console()
                common.loading_message_with_delay("Loading login form", 'green', 2)
                common.clear_console()
                common.print_main_header()  # Fixed main header for all the time
                common.print_sub_header("User Login System")
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                common.show_message_with_delay(auth.login_user(username, password))
            else:
                # Logout action
                common.show_message_with_delay(auth.logout_user(), "yellow")
        
        elif choice == "3":  # View Logs (Admin) or Exit
            if auth.is_logged_in():
                if auth.session["role"] == "admin":
                    # Admin: View logs option
                    common.show_message_with_delay("Viewing logs...", "cyan")
                    # Implement log viewing functionality here
                else:
                    common.show_message_with_delay("Logging out...", "yellow")
                    break
            else:
                common.show_message_with_delay("Goodbye!", "magenta")
                break

        elif choice == "4":  # Exit option (only when not logged in)
            common.show_message_with_delay("Goodbye!", "magenta")
            break

if __name__ == "__main__":
    main()
