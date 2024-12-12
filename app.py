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
                    if auth.session["role"] == "admin":
                        common.clear_console()
                        common.loading_message_with_delay("Users managing system is loading, please wait", 'green', 2)
                        while True:
                            common.clear_console()
                            common.print_main_header()  # Fixed main header
                            common.print_sub_header(f"Users Managing System")
                            print("1. View All Users")
                            print("2. Search User")
                            print("3. Update User Role")
                            print("5. View All Workers Only")
                            print("6. Back to Main Menu")
                            print("7. Logout")

                            choice = common.get_valid_number_input("Choose an option: ")
                            if choice == 1:
                                common.clear_console()
                                common.loading_message_with_delay("Viewing all users is loading, please wait", 'green', 2)
                                result = auth.view_all_users()
                                print(result)
                                common.wait_for_keypress()
                            elif choice == 2:
                                common.clear_console()
                                common.loading_message_with_delay("User searching form is loading, please wait", 'green', 2)                                
                                result = auth.search_user()
                                print(result)
                                common.wait_for_keypress()

                    else:
                       print(common.color_text("Only admin can manage users!!! Please login as a admin.", "red"))
                       continue
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
                    result = auth.logout_user()
                    common.show_message_with_delay(result)
                    show_logged_in_menu()
                else:
                    print(common.color_text("Invalid input choice. Please enter 1, 2, 3, 4 or 5 as valid menu number.", "red"))
                    continue
    else:
        # Non-logged-in options
        common.print_sub_header("User Authentication System")
        print("1. Login")
        print("2. Register")
        while True:
                choice = common.get_valid_number_input("Choose an option: ")
                if choice == 1:
                    common.clear_console()
                    common.loading_message_with_delay("Login form is loading, please wait", 'green', 2)
                    result = auth.login_user()
                    common.show_message_with_delay(result)
                    show_logged_in_menu()
                elif choice == 2:
                    
                    common.clear_console()
                    common.loading_message_with_delay("Register form is loading, please wait", 'green', 2)
                    result = auth.register_user()
                    common.show_message_with_delay(result)
                    show_logged_in_menu()
                else:
                    print(common.color_text("Invalid input choice. Please enter 1 or 2 as valid menu number.", "red"))
                    continue

def main():
    show_logged_in_menu()  # Display role-based menu

if __name__ == "__main__":
    main()
