import os
import re
import time
import sys

def color_text(text, color=None, style=None, bg_color=None):
    # ANSI escape codes for colors
    colors = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "reset": "\033[0m"
    }

    # ANSI escape codes for background colors
    bg_colors = {
        "black": "\033[40m",
        "red": "\033[41m",
        "green": "\033[42m",
        "yellow": "\033[43m",
        "blue": "\033[44m",
        "magenta": "\033[45m",
        "cyan": "\033[46m",
        "white": "\033[47m",
        "reset": "\033[0m"
    }

    # ANSI escape codes for styles
    styles = {
        "bold": "\033[1m",
        "italic": "\033[3m",
        "underline": "\033[4m",
        "strikethrough": "\033[9m",
        "dim": "\033[2m",
        "blinking": "\033[5m",
        "reverse": "\033[7m"
    }

    # Initialize the final text string
    final_text = ""

    # Apply color if specified
    if color in colors:
        final_text += colors[color]
    
    # Apply background color if specified
    if bg_color in bg_colors:
        if color == bg_color:
            return text  # Background and text color same provided that's why returnin without implecation
        final_text += bg_colors[bg_color]

    # Apply style if specified
    if style in styles:
        final_text += styles[style]
    
    # Add the actual text
    final_text += text

    # Reset color, style, and background color at the end
    final_text += colors["reset"]  # Reset color
    final_text += bg_colors["reset"]  # Reset background color
    final_text += "\033[0m"  # Reset style

    return final_text

# Example usage:
# print(color_text("This is bold and red text on a yellow background", color="black", style="bold", bg_color="green"))
# print(color_text("This is green text with blue background", color="green", bg_color="blue"))
# print(color_text("This is strikethrough text on a black background", style="strikethrough", bg_color="black"))
# print(color_text("This is normal text"))

def loading_message_with_delay(message, color="white", delay=2):
    """Display a loading message with an animated dot sequence and a delay, ensuring each dot has the same color."""
    # ANSI codes for different colors
    color_codes = {
        "black": 30, "red": 31, "green": 32, "yellow": 33,
        "blue": 34, "magenta": 35, "cyan": 36, "white": 37,
    }

    # Set the color code
    color_code = color_codes.get(color, 37)  # Default to white if color is not recognized

    # Print the message with color
    sys.stdout.write(f"\033[{color_code}m{message}\033[0m")
    sys.stdout.flush()  # Flush the output buffer to immediately display the message
    
    # Animate dots with the same color until the delay time is over
    start_time = time.time()
    while time.time() - start_time < delay:
        sys.stdout.write(f"\033[{color_code}m.\033[0m")  # Color the dot the same as the message
        sys.stdout.flush()  # Ensure the dot is immediately displayed
        time.sleep(0.5)  # Add a 0.5 second delay between each dot
    
    # Move to the next line after the loading animation
    sys.stdout.write("\n")
    sys.stdout.flush()



# Input Validation
def get_valid_input(prompt, valid_options=None):
    while True:
        user_input = input(prompt).strip()
        if valid_options and user_input.lower() not in valid_options:
            print(color_text("Invalid choice. Please try again.", "red"))
        else:
            return user_input

def get_valid_text_input(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input:  # Check if the input is not empty
            return user_input
        else:
            print(color_text("Invalid input. Please enter some text.", "red"))

def get_valid_number_input(prompt):
    while True:
        user_input = input(prompt).strip()
        # Check if the input is a valid number using regular expression
        if re.match(r"^[0-9]+(\.[0-9]+)?$", user_input):
            return float(user_input) if '.' in user_input else int(user_input)
        else:
            print(color_text("Invalid input. Please enter a valid number.", "red"))

# Example usage:
# name = get_valid_text_input("Enter your name: ")
# age = get_valid_number_input("Enter your age: ")
# print(f"Hello {name}, your age is {age}.")

# Function for main header
def print_main_header():
    
    header_text = "SmartPanda Dashboard"

    print(color_text("=" * 50, color="white", style="dim", bg_color="blue"))
    print(color_text(header_text.center(50), color="white", bg_color="blue"))
    print(color_text("=" * 50, color="white", style="dim", bg_color="blue"))

# Function for sub header
def print_sub_header(sub_title):
    print(color_text("-" * 50, style="dim", bg_color=""))
    print(color_text(sub_title.center(50), bg_color="white"))
    print(color_text("-" * 50, style="dim", bg_color=""))

# Formatting Numbers (Currency)
def format_currency(amount):
    return f"₩{amount:,.2f}"

def calculate_vat_and_tax(amount, vat_rate=0.15, tax_rate=0.05):
    """
    Calculate VAT and tax for a given amount.

    Parameters:
    - amount (float): The base amount to calculate VAT and tax on.
    - vat_rate (float): The VAT rate as a decimal (default is 15%).
    - tax_rate (float): The tax rate as a decimal (default is 5%).

    Returns:
    - dict: A dictionary containing VAT, tax, and the total amount.
    """
    vat = amount * vat_rate
    tax = amount * tax_rate
    total = amount + vat + tax
    return {"vat": vat, "tax": tax, "total": total}

# Clear Console
def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

# Show Message with Delay
def show_message_with_delay(message, color="white", delay=2):
    print(color_text(message, color))
    time.sleep(delay)

def wait_for_keypress():
    """Wait for the user to press Enter."""
    input("\nPress Enter to continue...")


# Get Valid Username
def get_valid_username(auth):
    while True:
        username = input("Enter a username: ").strip()
        if not re.match(r"^[a-zA-Z0-9_]{3,20}$", username):
            print(color_text("Invalid username. Use 3-20 alphanumeric characters or underscores.", "red"))
        elif not auth.is_unique("username", username):
            print(color_text("Username already exists. Please try another.", "red"))
        else:
            return username

# Get Valid Email
def get_valid_email(auth):
    while True:
        email = input("Enter your email: ").strip()
        if not re.match(r"^[\w.-]+@[a-zA-Z\d.-]+\.[a-zA-Z]{2,}$", email):
            print(color_text("Invalid email format. Please try again.", "red"))
        elif not auth.is_unique("email", email):
            print(color_text("Email already exists. Please try another.", "red"))
        else:
            return email

# Get Valid Phone Number
def get_valid_phone(auth):
    while True:
        phone = input("Enter your phone number: ").strip()
        if not re.match(r"^\d{10,15}$", phone):
            print(color_text("Invalid phone number. Must be 10-15 digits.", "red"))
        elif not auth.is_unique("phone", phone):
            print(color_text("Phone number already exists. Please try another.", "red"))
        else:
            return phone
