elif choice == 2:
                                common.clear_console()
                                common.loading_message_with_delay("User searching form is loading, please wait", 'green', 2)                                
                                result = auth.search_user()
                                print(result)
                                common.wait_for_keypress()