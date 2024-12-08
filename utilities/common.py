import os

# Text Coloring
def color_text(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "reset": "\033[0m"
    }
    return f"{colors.get(color, colors['reset'])}{text}{colors['reset']}"

# Text Styling
def style_text(text, style):
    styles = {
        "bold": "\033[1m",
        "italic": "\033[3m",
        "underline": "\033[4m",
        "strikethrough": "\033[9m",
        "dim": "\033[2m",
        "blinking": "\033[5m",
        "reverse": "\033[7m"
    }
    return f"{styles.get(style, styles['reset'])}{text}{styles['reset']}"


# Input Validation
def get_valid_input(prompt, valid_options=None):
    while True:
        user_input = input(prompt).strip()
        if valid_options and user_input.lower() not in valid_options:
            print(color_text("Invalid choice. Please try again.", "red"))
        else:
            return user_input

# Formatting Numbers (Currency)
def format_currency(amount):
    return f"${amount:,.2f}"

# Clear Console
def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

# Error Logging
def log_error(message):
    with open("error_log.txt", "a") as log_file:
        log_file.write(f"{message}\n")
    print(color_text("An error occurred. Check error_log.txt for details.", "red"))

# Reusable Headers/Footers for Menus
def print_header(title):
    print(color_text("=" * 50, "yellow"))
    print(color_text(title.center(50), "cyan"))
    print(color_text("=" * 50, "yellow"))

def print_footer():
    print(color_text("-" * 50, "magenta"))

# Display Menu (Example)
def display_menu(menu_items):
    print_header("SmartPanda Menu")
    for idx, item in enumerate(menu_items, start=1):
        print(f"{idx}. {item}")
    print_footer()

# Example Usage
# if __name__ == "__main__":
#     # Example menu for testing
#     sample_menu = ["Add Item", "Update Item", "Delete Item", "View Orders", "Exit"]

#     # Clear console and display menu
#     clear_console()
#     display_menu(sample_menu)

#     # Get user input
#     choice = get_valid_input("Enter your choice (1-5): ", ["1", "2", "3", "4", "5"])
#     print(color_text(f"You selected: {sample_menu[int(choice)-1]}", "green"))
