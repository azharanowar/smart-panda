import json
import os
import utilities.common as common

class Inventory:
    def __init__(self):
        self.products = self.load_products()

    def load_products(self):
        """Load products from the products.json file."""
        if os.path.exists("products.json"):
            with open("products.json", "r") as file:
                return json.load(file)
        return []

    def save_products(self):
        """Save the products to the products.json file."""
        with open("products.json", "w") as file:
            json.dump(self.products, file, indent=4)

    def add_product(self):
        """Add a new product to the inventory."""
        common.clear_console()
        common.print_main_header()
        common.print_sub_header("Add Product")

        # Get valid product name
        name = common.get_valid_text_input("Enter product name: ")

        # Get valid price and quantity
        price = common.get_valid_number_input("Enter product price: ")
        quantity = common.get_valid_number_input("Enter product quantity: ")

        # Category selection with validation
        categories = ["Snacks", "Lunch", "Dinner", "Drinks", "Desserts"]
        print("Select a category:")
        category_id = 0
        for category in categories:
            category_id = category_id + 1
            print(f"{category_id}. {category}")
        
        category_choice = common.get_valid_number_input("Enter the number corresponding to the category: ")
        if category_choice < 1 or category_choice > len(categories):
            print(common.color_text("Invalid category selection.", "red"))
            category_choice = common.get_valid_number_input("Enter the number corresponding to the category: ")

        category = categories[category_choice - 1]

        # Input extras with price, with validation
        extras = []
        while True:
            extra_name = common.get_valid_text_input("Enter extra item name (or Enter x to finish): ")
            if not extra_name or (extra_name == "X" or extra_name == "x"):
                break
            extra_price = common.get_valid_number_input(f"Enter price for {extra_name}: ")
            extras.append({"name": extra_name, "price": extra_price})

        # Assigning ID to the product
        product_id = len(self.products) + 1

        product = {
            "id": product_id,
            "name": name,
            "price": price,
            "quantity": quantity,
            "category": category,
            "extras": extras
        }

        self.products.append(product)
        self.save_products()
        print(common.color_text(f"Product '{name}' added successfully!", "green", style="bold"))

    def view_all_products(self, category=None):
        """View all products, optionally filtered by category."""
        common.clear_console()
        common.print_main_header()
        common.print_sub_header("View Products")

        filtered_products = self.products if not category else [product for product in self.products if product["category"].lower() == category.lower()]

        if not filtered_products:
            return common.color_text("No products found.", color="yellow", style="italic")

        name_width = 20
        price_width = 10
        quantity_width = 10
        category_width = 15
        extras_width = 20

        # Header with blue background
        header = common.color_text(f"{'ID':<5}{'Name':<{name_width}}{'Price':<{price_width}}{'Quantity':<{quantity_width}}{'Category':<{category_width}}{'Extras':<{extras_width}}", bg_color="blue", style="bold")
        
        # Create separator line
        separator = "-" * 85

        # Format each product row to match the fixed column widths
        rows = "\n".join(
            f"{product['id']:<5}{product['name']:<{name_width}}{common.format_currency(product['price']):<{price_width}}{product['quantity']:<{quantity_width}}{product['category']:<{category_width}}{', '.join([extra['name'] for extra in product['extras']]):<{extras_width}}"
            for product in filtered_products
        )

        return f"{header}\n{separator}\n{rows}"

    def search_product(self):
        """Search for a product by ID, name, or category."""
        common.clear_console()
        common.print_main_header()
        common.print_sub_header("Search Product")

        search_key = input("Search by product ID, name, or category: ").lower()

        # Search for the product by ID, name, or category
        results = [
            product for product in self.products
            if search_key in str(product["id"]) or search_key in product["name"].lower() or search_key in product["category"].lower()
        ]

        if not results:
            return common.color_text(f"No products found matching '{search_key}'.", color="yellow")

        return self.view_products_by_list(results)


    def update_product(self):
        """Update product details."""
        common.clear_console()
        common.print_main_header()
        common.print_sub_header("Update Product")

        product_id = int(input("Enter the product ID to update: "))

        product_to_update = next((product for product in self.products if product["id"] == product_id), None)

        if not product_to_update:
            return common.color_text(f"Product with ID '{product_id}' not found.", color="yellow")

        print(f"Updating product: {product_to_update['name']}")
        new_name = input(f"Enter new name (current: {product_to_update['name']}): ")
        new_price = float(input(f"Enter new price (current: {product_to_update['price']}): "))
        new_quantity = int(input(f"Enter new quantity (current: {product_to_update['quantity']}): "))
        
        
        categories = ["Snacks", "Lunch", "Dinner", "Drinks", "Desserts"]
        print("Select a category:")
        category_id = 0
        for category in categories:
            category_id = category_id + 1
            print(f"{category_id}. {category}")
        
        category_choice = common.get_valid_number_input(f"Enter the category number (current: {product_to_update['category']}): ")
        if category_choice < 1 or category_choice > len(categories):
            print(common.color_text("Invalid category selection.", "red"))
            category_choice = common.get_valid_number_input(f"Enter the category number (current: {product_to_update['category']}): ")

        new_category = categories[category_choice - 1]

        # Handle updating extras (optional)
        print(f"Current extras: {', '.join([extra['name'] for extra in product_to_update['extras']])}")
        new_extras = []
        while True:
            extra_name = common.get_valid_text_input("Enter extra item name (or Enter x to finish): ")
            if not extra_name or (extra_name == "X" or extra_name == "x"):
                break
            extra_price = common.get_valid_number_input(f"Enter price for {extra_name}: ")
            new_extras.append({"name": extra_name, "price": extra_price})

        product_to_update.update({
            "name": new_name or product_to_update["name"],
            "price": new_price or product_to_update["price"],
            "quantity": new_quantity or product_to_update["quantity"],
            "category": new_category or product_to_update["category"],
            "extras": new_extras or product_to_update["extras"]
        })

        self.save_products()
        return common.color_text(f"Product '{product_to_update['name']}' updated successfully.", "green", style="bold")

    def delete_product(self):
        """Delete a product from the inventory."""
        common.clear_console()
        common.print_main_header()
        common.print_sub_header("Delete Product")

        product_id = int(input("Enter the product ID to delete: "))

        product_to_delete = next((product for product in self.products if product["id"] == product_id), None)

        if not product_to_delete:
            return common.color_text(f"Product with ID '{product_id}' not found.", color="yellow")

        confirmation = input(f"Are you sure you want to delete the product '{product_to_delete['name']}'? (y/n): ").lower()

        if confirmation != 'y':
            return common.color_text("Product deletion canceled.", color="yellow")

        self.products.remove(product_to_delete)
        self.save_products()
        return common.color_text(f"Product '{product_to_delete['name']}' deleted successfully.", "green", style="bold")

    def view_products_by_list(self, product_list):
        """Helper method to view products from a provided list."""
        name_width = 20
        price_width = 10
        quantity_width = 10
        category_width = 15
        extras_width = 20

        # Header with blue background
        header = common.color_text(f"{'ID':<5}{'Name':<{name_width}}{'Price':<{price_width}}{'Quantity':<{quantity_width}}{'Category':<{category_width}}{'Extras':<{extras_width}}", bg_color="blue", style="bold")
        
        # Create separator line
        separator = "-" * 85

        # Format each product row to match the fixed column widths
        rows = "\n".join(
            f"{product['id']:<5}{product['name']:<{name_width}}{common.format_currency(product['price']):<{price_width}}{product['quantity']:<{quantity_width}}{product['category']:<{category_width}}{', '.join([extra['name'] for extra in product['extras']]):<{extras_width}}"
            for product in product_list
        )

        return f"{header}\n{separator}\n{rows}"
