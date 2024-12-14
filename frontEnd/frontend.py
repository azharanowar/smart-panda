import json
import random
import utilities.common as common

class Frontend:
    def __init__(self, products_file="data/products.json", orders_file="data/orders.json"):
        self.products_file = products_file
        self.orders_file = orders_file
        self.products = self.load_products()
        self.orders = self.load_orders()

    def load_products(self):
        """Load products from the JSON file."""
        try:
            with open(self.products_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Error: Products file is corrupted. Starting with an empty inventory.")
            return []

    def load_orders(self):
        """Load orders from the specified JSON file."""
        try:
            with open(self.orders_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Error: Orders file is corrupted. Starting with an empty order list.")
            return []

    def save_orders(self):
        """Save orders to the orders JSON file."""
        try:
            with open(self.orders_file, "w") as file:
                json.dump(self.orders, file, indent=4)
        except FileNotFoundError:
            print("Error: Unable to save orders. Ensure the directory exists.")

    def new_order(self):
        """Create a new order by selecting products and checkout."""
        common.clear_console()
        common.print_main_header()
        common.print_sub_header("Place New Order")

        # Show products by category
        print("Select what you want to have:")
        category_choice = 1
        categories = []
        for product in self.products:
            if product['category'] not in categories:
                categories.append(product['category'])
                print(f"{category_choice}. {product['category']}")
                category_choice += 1

        category_id = common.get_valid_number_input("Enter the number corresponding to the category: ")
        if category_id < 1 or category_id > len(categories):
            print(common.show_message_with_delay("Invalid category selection. Try again", "red"))
            return

        category = categories[category_id - 1]

        # Show products in the selected category
        available_products = []
        for product in self.products:
            if product['category'].lower() == category.lower():
                available_products.append(product)

        print(common.color_text(f"\nProducts in '{category}' category:", bg_color="blue"))
        print(common.color_text("--------------------------------", style="dim"))
        for product in available_products:
            print(common.color_text(f"{product['id']}. {product['name']} - {common.format_currency(product['price'])} (Stock: {product['quantity']})", style='bold'))

        # Add products to cart
        cart = []
        while True:
            product_id = common.get_valid_number_input("Enter product ID to add to cart (0 to finish): ")
            if product_id == 0:
                break

            product = None
            for available_product in available_products:
                if available_product['id'] == product_id:
                    product = available_product
                    break

            if product:
                quantity = common.get_valid_number_input(f"Enter quantity for {product['name']}: ")
                if product['quantity'] >= quantity:
                    cart.append({"product_id": product['id'], "name": product['name'], "price": product['price'], "quantity": quantity})
                    print(common.color_text(f"{product['name']} added to cart.", color='green', style='bold'))
                else:
                    print(common.color_text(f"Not enough stock for {product['name']}. Available stock: {product['quantity']}", "red"))
            else:
                print(common.color_text("Invalid product ID.", "red"))

        # Checkout
        if cart:
            order_id = f"#SP{random.randint(1000, 9999)}"
            total_price = sum(item['price'] * item['quantity'] for item in cart)
            print(f"\nYour order ID: {common.color_text(order_id, bg_color='blue', style='bold')}")
            print(f"Total: {common.color_text(common.format_currency(total_price), bg_color='blue', style='bold')}")

            payment_method = input("Choose payment method (1. Bank Transfer, 2. Credit Card): ")
            if payment_method == '1':
                print(common.color_text(f"Payment successful with Bank transfer! Order {order_id} placed.", color='green'))
            elif payment_method == '2':
                print(common.color_text(f"Payment successful with card! Order {order_id} placed.", color='green'))
            else:
                print(common.color_text("Invalid payment method.", "red"))
                return

            order = {
                "order_id": order_id,
                "cart": cart,
                "total_price": total_price,
                "payment_method": "Bank Transfer" if payment_method == '1' else "Credit Card",
                "status": "Pending"  # Default status is Pending
            }
            self.orders.append(order)
            self.save_orders()
        else:
            print(common.color_text("No products selected for the order.", "red"))



    def view_all_orders(self):
        """View all orders."""
        common.clear_console()
        common.print_main_header()
        common.print_sub_header("View Orders")

        if not self.orders:
            print(common.color_text("No orders found.", "yellow"))
            return

        print("Order ID | Total Price | Payment Method | Status")
        print("-" * 60)
        for order in self.orders:
            print(f"{common.color_text(order['order_id'], 'white', bg_color='blue', style='bold')} | {common.format_currency(order['total_price'])} | {order['payment_method']} | {order['status']}")

    def update_order(self):
        """Update an existing order."""
        common.clear_console()
        common.print_main_header()
        common.print_sub_header("Update Order")

        order_id = input("Enter the order ID to update: ")
        order_to_update = next((order for order in self.orders if order['order_id'] == order_id), None)

        if not order_to_update:
            print(common.color_text(f"Order with ID '{order_id}' not found.", "yellow"))
            return

        print(f"Updating Order: {order_id}")
        # Here, you can add logic to update order details
        order_to_update["status"] = "Updated"  # Example of updating order status
        self.save_orders()
        print(common.color_text(f"Order '{order_id}' updated successfully.", "green", style="bold"))
