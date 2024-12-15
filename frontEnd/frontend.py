import json
import random
import utilities.common as common
import user_authentication.user_auth as user_auth_management

class Frontend:
    def __init__(self, products_file="data/products.json", orders_file="data/orders.json"):
        self.products_file = products_file
        self.orders_file = orders_file
        self.products = self.load_products()
        self.orders = self.load_orders()
        user_auth = user_auth_management.UserAuth()
        self.current_user = user_auth.session.get("username")  # Fetch the current user's username
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

    def save_products(self):
        """Save the updated product list to the products JSON file."""
        try:
            with open(self.products_file, "w") as file:
                json.dump(self.products, file, indent=4)
        except FileNotFoundError:
            print("Error: Unable to save products. Ensure the directory exists.")

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
        """Save the current list of orders to a JSON file."""
        try:
            with open(self.orders_file, "w") as file:
                json.dump(self.orders, file, indent=4)
            print(common.color_text("Your orders placed successfully.", bg_color='blue', style='bold'))
        except Exception as e:
            print(common.color_text("Error placing the order. Please try again.", color='red', style='bold'))


    def new_order(self):
        """Create a new order by selecting products and checkout."""
        common.clear_console()
        common.print_main_header()
        common.print_sub_header("Place New Order")

        # Show products by category
        print("Select what you want to have now:")
        category_choice = 1
        categories = []
        for product in self.products:
            if product['category'] not in categories:
                categories.append(product['category'])
                print(f"{category_choice}. {product['category']}")
                category_choice += 1

        category_id = common.get_valid_number_input("Enter the number corresponding to the category: ")
        if category_id < 1 or category_id > len(categories):
            common.show_message_with_delay("Invalid category selection. Try again", "red")
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
                    # Add extras
                    extras = []
                    if "extras" in product and product["extras"]:
                        print("Available extras:")
                        for idx, extra in enumerate(product["extras"], start=1):
                            print(f"{idx}. {extra['name']} - {common.format_currency(extra['price'])}")
                        while True:
                            extra_choice = common.get_valid_number_input("Enter extra number to add (0 to finish): ")
                            if extra_choice == 0:
                                break
                            if 1 <= extra_choice <= len(product["extras"]):
                                extras.append(product["extras"][extra_choice - 1])
                            else:
                                common.show_message_with_delay("Invalid extra selection. Try again.", "red")

                    # Add product to cart
                    cart.append({
                        "product_id": product['id'],
                        "name": product['name'],
                        "price": product['price'],
                        "quantity": quantity,
                        "extras": extras
                    })
                    common.show_message_with_delay(f"{product['name']} added to cart.", color='green')
                else:
                    common.show_message_with_delay(f"Not enough stock for {product['name']}. Available stock: {product['quantity']}", "red")
            else:
                common.show_message_with_delay("Invalid product ID.", "red")

        # Checkout
        if cart:
            order_id = f"#SP{random.randint(1000, 9999)}"
            base_total = sum(item['price'] * item['quantity'] for item in cart)
            extras_total = sum(extra['price'] for item in cart for extra in item['extras'])

            # Calculate VAT and Tax
            vat_tax_details = common.calculate_vat_and_tax(base_total + extras_total)
            total_price = vat_tax_details['total']

            # Display order summary
            print(f"\nYour order ID: {common.color_text(order_id, bg_color='blue', style='bold')}")
            print(f"Subtotal: {common.color_text(common.format_currency(base_total), bg_color='blue', style='bold')}")
            print(f"Extras: {common.color_text(common.format_currency(extras_total), bg_color='blue')}")
            print(f"VAT (15%): {common.color_text(common.format_currency(vat_tax_details['vat']), bg_color='blue')}")
            print(f"Tax (5%): {common.color_text(common.format_currency(vat_tax_details['tax']), bg_color='blue')}")
            print(f"Total: {common.color_text(common.format_currency(total_price), bg_color='blue', style='bold')}")

            payment_method = input("Choose payment method (1. Bank Transfer, 2. Credit Card): ")
            if payment_method == '1':
                common.show_message_with_delay(f"Payment successful with Bank transfer! Order {order_id} placed.", color='green')
            elif payment_method == '2':
                card_info = input("Enter your credit card info: ")
                common.show_message_with_delay(f"Payment successful with card! Order {order_id} placed.", color='green')
            else:
                common.show_message_with_delay("Invalid payment method selected. Try again", "red")
                return

            order = {
                "order_id": order_id,
                "username": self.current_user,  # Add username to the order
                "cart": cart,
                "base_total": base_total,
                "extras_total": extras_total,
                "vat": vat_tax_details['vat'],
                "tax": vat_tax_details['tax'],
                "total_price": total_price,
                "payment_method": "Bank Transfer" if payment_method == '1' else "Credit Card",
                "status": "Pending"  # Default status is Pending
            }
            self.orders.append(order)
            self.save_orders()


            # Save the updated product list
            for item in cart:
                for product in self.products:
                    if product['id'] == item['product_id']:
                        product['quantity'] -= item['quantity']
            self.save_products()

        else:
            common.show_message_with_delay("No products selected for the order.", "red")

    def view_my_orders(self):
        """View all orders placed by the current user."""
        common.clear_console()
        common.print_main_header()
        common.print_sub_header("My Orders")

        if not self.orders:
            print(common.color_text("No orders found.", color="red"))
            return

        user_orders = []
        for order in self.orders:
            if order['username'] == self.current_user:
                user_orders.append(order)

        if not user_orders:
            print(common.color_text("No orders found for the current user.", color="red"))
            return

        for order in user_orders:
            print(common.color_text(f"Order ID: {order['order_id']}", bg_color="blue", style="bold"))
            print("Items:")
            for item in order['cart']:
                # Handling missing 'extras' key
                extras = ", ".join(extra['name'] for extra in item.get('extras', [])) if item.get('extras') else "None"
                print(f"- {item['name']} (Quantity: {item['quantity']}, Price: {common.format_currency(item['price'])}, Extras: {extras})")
            print(f"Subtotal: {common.format_currency(order['base_total'])}")
            print(f"Extras Total: {common.format_currency(order['extras_total'])}")
            print(f"VAT: {common.format_currency(order['vat'])}")
            print(f"Tax: {common.format_currency(order['tax'])}")
            print(f"Total Price: {common.format_currency(order['total_price'])}")
            print(f"Payment Method: {order['payment_method']}")
            print(f"Status: {order['status']}")
            print(common.color_text("-" * 40, style="dim"))


    def cancel_order(self):
        """Cancel an order by its order ID."""
        self.view_my_orders()
        order_id = input("Enter the Order ID to cancel: ").strip()

        user_orders = [order for order in self.orders if order['username'] == self.current_user]

        for order in user_orders:
            if order['order_id'] == order_id:
                # Restock the products
                for item in order['cart']:
                    for product in self.products:
                        if product['id'] == item['product_id']:
                            product['quantity'] += item['quantity']

                self.orders.remove(order)
                self.save_orders()
                self.save_products()
                common.show_message_with_delay(f"Order {order_id} has been canceled.", "green")
                return

        common.show_message_with_delay("Order ID not found. Please try again.", "red")

    def update_order(self):
        """Update an existing order by first canceling it and placing a new one."""
        self.view_my_orders()
        order_id = input("Enter the Order ID to update: ").strip()

        user_orders = [order for order in self.orders if order['username'] == self.current_user]

        for order in user_orders:
            if order['order_id'] == order_id:
                # Restock the products
                for item in order['cart']:
                    for product in self.products:
                        if product['id'] == item['product_id']:
                            product['quantity'] += item['quantity']

                self.orders.remove(order)
                self.save_orders()
                self.save_products()
                common.show_message_with_delay(f"Order {order_id} has been canceled. You can now place a new order.", "green")
                self.new_order()
                return

        common.show_message_with_delay("Order ID not found. Please try again.", "red")
