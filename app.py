import utilities.common as common
import user_authentication.user_auth as user_auth
import inventory_management.inventory as inventory_management
import frontEnd.frontend as frontend_management

auth = user_auth.UserAuth()
def dashboard_menu():
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
                    inventory = inventory_management.Inventory()
                    common.clear_console()
                    common.loading_message_with_delay("Inventory management system is loading, please wait", 'green', 2)
                    while True:
                        common.clear_console()
                        common.print_main_header()  # Fixed main header
                        common.print_sub_header(f"Inventory Management System")
                        print("1. Add Product")
                        print("2. View All Products")
                        print("3. Search Product")
                        print("4. Update Product")
                        print("5. Delete Product")
                        print("6. Logout")
                        print("0. Back to Main Menu")

                        choice = common.get_valid_number_input("Choose an option: ")
                        if choice == 1:
                            common.clear_console()
                            common.loading_message_with_delay("Adding product, please wait", 'green', 2)
                            result = inventory.add_product()
                            print(result)
                            common.wait_for_keypress()
                        elif choice == 2:
                            common.clear_console()
                            common.loading_message_with_delay("Viewing all products, please wait", 'green', 2)
                            result = inventory.view_all_products()
                            print(result)
                            common.wait_for_keypress()
                        elif choice == 3:
                            common.clear_console()
                            common.loading_message_with_delay("Searching product, please wait", 'green', 2)
                            result = inventory.search_product()
                            print(result)
                            common.wait_for_keypress()
                        elif choice == 4:
                            common.clear_console()
                            common.loading_message_with_delay("Updating product, please wait", 'green', 2)
                            result = inventory.update_product()
                            print(result)
                            common.wait_for_keypress()
                        elif choice == 5:
                            common.clear_console()
                            common.loading_message_with_delay("Deleting product, please wait", 'green', 2)
                            result = inventory.delete_product()
                            print(result)
                            common.wait_for_keypress()
                        elif choice == 6:
                            common.clear_console()
                            common.loading_message_with_delay("Logging out, please wait", "blue", 2)
                            common.clear_console()
                            result = auth.logout_user()
                            common.show_message_with_delay(result)
                            dashboard_menu()
                        elif choice == 0:
                            dashboard_menu()
                        else:
                            print(common.show_message_with_delay("Invalid input choice. Please enter valid menu number.", "red"))
                            continue

                elif choice == 2:
                    common.clear_console()
                    common.loading_message_with_delay("Workers order management system is loading, please wait", 'green', 2)
                    frontend = frontend_management.Frontend()
                    while True:
                        common.clear_console()
                        common.print_main_header()
                        common.print_sub_header("Order Management System Backend")
                        print("1. View All Orders")
                        print("2. Update Order Status")
                        print("3. Cancel Order")
                        print("4. Logout")
                        print("0. Back to Main Menu")

                        choice = common.get_valid_number_input("Choose an option: ")
                        if choice == 1:
                            frontend.view_all_orders()
                            common.wait_for_keypress()
                        elif choice == 2:
                            frontend.update_order_status()
                            common.wait_for_keypress()
                        elif choice == 3:
                            frontend.cancel_order()
                            common.wait_for_keypress()
                        elif choice == 4:
                            common.clear_console()
                            common.loading_message_with_delay("Logging out, please wait", "blue", 2)
                            common.clear_console()
                            result = auth.logout_user()
                            common.show_message_with_delay(result)
                            dashboard_menu()
                        elif choice == 0:
                            dashboard_menu()
                        else:
                            common.show_message_with_delay("Invalid input choice. Please enter valid menu number.", "red")
                            continue
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
                            print("3. Delete User")
                            print("4. Update User Role")
                            print("5. View All Workers Only")
                            print("6. Logout")

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
                            elif choice == 3:
                                common.clear_console()
                                common.loading_message_with_delay("Delete user is loading, please wait", 'green', 2)                                
                                result = auth.delete_user()
                                print(result)
                                common.wait_for_keypress()
                            elif choice == 4:
                                common.clear_console()
                                common.loading_message_with_delay("Update user role is loading, please wait", 'green', 2)                                
                                result = auth.update_role()
                                print(result)
                                common.wait_for_keypress()
                            elif choice == 5:
                                common.clear_console()
                                common.loading_message_with_delay("View all workers is loading, please wait", 'green', 2)                                
                                result = auth.view_all_workers()
                                print(result)
                                common.wait_for_keypress()
                            elif choice == 6:
                                common.clear_console()
                                common.loading_message_with_delay("Logging out is loading, please wait", "blue", 2)
                                common.clear_console()
                                result = auth.logout_user()
                                common.show_message_with_delay(result)
                                dashboard_menu()
                            else:
                                print(common.show_message_with_delay("Invalid input choice. Please enter valid menu number.", "red"))
                                continue

                    else:
                       print(common.color_text("Only admin can manage users!!! Please login as a admin.", "red"))
                       continue
                elif choice == 4:
                    common.clear_console()
                    common.loading_message_with_delay("Logging out is loading, please wait", "blue", 2)
                    common.clear_console()
                    result = auth.logout_user()
                    common.show_message_with_delay(result)
                    dashboard_menu()
                else:
                    print(common.color_text("Invalid input choice. Please enter 1, 2, 3, or 4 as valid menu number.", "red"))
                    continue
        else:
            # Customer Dashboard
            while True:
                common.clear_console()
                common.print_main_header()  # Fixed main header
                common.print_sub_header(f"Customer Dashboard")
                frontend = frontend_management.Frontend()
                print("1. New Order")
                print("2. View My Orders")
                print("3. Update Order")
                print("4. Cancel Order")
                print("5. Panda Assistant (Voice Assistance)")
                print("6. Logout")

                choice = common.get_valid_number_input("Choose an option: ")
                if choice == 1:
                    frontend.new_order()
                elif choice == 2:
                    result = frontend.view_my_orders()
                    print(result)
                    common.wait_for_keypress()
                elif choice == 3:
                    result = frontend.update_order()
                    print(result)
                    common.wait_for_keypress()
                elif choice == 4:
                    result = frontend.cancel_order()
                    print(result)
                    common.wait_for_keypress()
                elif choice == 5:
                    import voice_ordering.panda_assistant as panda_assistant
                    panda = panda_assistant.PandaAssistant()
                    panda.starting()
                elif choice == 6:
                    common.clear_console()
                    common.loading_message_with_delay("Logging out, please wait", "blue", 2)
                    common.clear_console()
                    result = auth.logout_user()
                    common.show_message_with_delay(result)
                    dashboard_menu()
                else:
                    print(common.show_message_with_delay("Invalid input choice. Please enter valid menu number.", "red"))
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
                    dashboard_menu()
                elif choice == 2:
                    
                    common.clear_console()
                    common.loading_message_with_delay("Register form is loading, please wait", 'green', 2)
                    result = auth.register_user()
                    common.show_message_with_delay(result)
                    dashboard_menu()
                else:
                    print(common.color_text("Invalid input choice. Please enter 1 or 2 as valid menu number.", "red"))
                    continue

def main():
    dashboard_menu()  # Display role-based menu

if __name__ == "__main__":
    main()
