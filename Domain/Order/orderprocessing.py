import json
import os
from Domain.menu.menucard import MenuManager
from Domain.Bill.generatingbill import generatingBill
from Domain.Table.bookingtable import tableBookingMenu
from Report.revenue import monthlyReport
from datetime import datetime
from Logs.log import error_logs

MENU_FILE = "Database/menu.json"
ORDER_FILE = "Database/orders.json"

class OrderManager:

    def __init__(self):
        if not os.path.exists(ORDER_FILE):
            with open(ORDER_FILE, "w") as f:
                json.dump([], f)

    def loadOrder(self):
        if not os.path.exists(ORDER_FILE):
            return []
        with open(ORDER_FILE) as file:
            return json.load(file)

    def saveOrder(self, orders):
        with open(ORDER_FILE, "w") as file:
            json.dump(orders, file, indent=4)

    def takeOrder(self):
        try:
            menu_mgr = MenuManager()
            menu = menu_mgr.loadMenu()
            if not menu:
                print("Menu is empty. Ask admin to add items.")
                return

            customerName = input("Enter customer name: ").strip()
            if not customerName:
                print("Customer name cannot be empty.")
                return

            orderItems = []
            total = 0.0

            menu_mgr.displayMenu()

            while True:
                itemName = input("\nEnter item name to add (or type 'done'): ").strip().lower()
                if itemName == "done":
                    break

                all_items = []
                for category, items in menu.items():
                    for item in items:
                        if "name" in item:
                            all_items.append(item)

                matched_item = next((i for i in all_items if i["name"].lower() == itemName), None)

                if not matched_item:
                    print("Item not found in menu.")
                    continue

                try:
                    if "half_price" in matched_item and "full_price" in matched_item:
                        portion = input("Do you want Half or Full? (h/f): ").strip().lower()
                        if portion == "h":
                            selected_price = float(matched_item["half_price"])
                            portion_name = "Half"
                        elif portion == "f":
                            selected_price = float(matched_item["full_price"])
                            portion_name = "Full"
                        else:
                            print("Invalid choice, skipping item.")
                            continue
                    else:
                        selected_price = matched_item.get("price")
                        if selected_price is None:
                            print("This item has no valid price entry. Skipping.")
                            continue
                        selected_price = float(selected_price)
                        portion_name = "Single"

                    quantity_str = input(f"Enter quantity for {matched_item['name']} ({portion_name}): ").strip()
                    if not quantity_str.isdigit():
                        print("Quantity must be a number.")
                        continue

                    qty = int(quantity_str)
                    if qty <= 0 or qty > 50:
                        print("Quantity must be between 1 and 50.")
                        continue

                    item_total = selected_price * qty
                    total += item_total

                    orderItems.append({
                        "itemId": matched_item["id"],
                        "name": matched_item["name"],
                        "portion": portion_name,
                        "price": selected_price,
                        "quantity": qty
                    })

                    print(f"Added {matched_item['name']} ({portion_name}) x {qty} = ₹{item_total}")

                except Exception as e:
                    print(f"Error adding item: {e}")

            if not orderItems:
                print("No items selected. Order Cancelled.")
                return

            use_custom = input("Enter custom date/time? (y/n): ").strip().lower()
            if use_custom == "y":
                dt_input = input("Enter date and time (YYYY-MM-DD HH:MM:SS): ").strip()
                try:
                    order_datetime = datetime.strptime(dt_input, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    print("Invalid format. Using current date/time instead.")
                    order_datetime = datetime.now()
            else:
                order_datetime = datetime.now()
                
            all_orders = self.loadOrder()
            orderId = len(all_orders) + 1

            order = {
                "order_id": orderId,
                "customer_name": customerName,
                "items": orderItems,
                "total": total,
                "status": "pending",
                "datetime": order_datetime.strftime("%Y-%m-%d %H:%M:%S")
            }

            all_orders.append(order)
            self.saveOrder(all_orders)

            print(f"\nOrder placed successfully! Total amount = ₹{total}")

        except Exception as e:
            error_logs(e)

    def viewAllOrders(self):
        orders = self.loadOrder()
        if not orders:
            print("No orders found.")
            return

        print("\n------ All Orders ------")
        for order in orders:
            print(f"\nOrder ID: {order['order_id']}, Customer: {order['customer_name']}, Total: ₹{order['total']}")
            for item in order["items"]:
                subtotal = item["price"] * item["quantity"]
                print(f"  {item['name']} ({item.get('portion','-')}) x {item['quantity']} = ₹{subtotal}")
            print("-" * 40)

    def staffMenu(self):
        while True:
            print("\n------ Staff Menu ------")
            print("1 - Take order")
            print("2 - View all orders")
            print("3 - Generate bill")
            print("4 - Table booking")
            print("5 - Monthly Sales Report")
            print("6 - Exit")

            try:
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    self.takeOrder()
                elif choice == 2:
                    self.viewAllOrders()
                elif choice == 3:
                    generatingBill()
                elif choice == 4:
                    tableBookingMenu()
                elif choice == 5:
                    monthlyReport()
                elif choice == 6:
                    break
                else:
                    print("Invalid choice, try again.")
            except ValueError:
                print("Enter a valid number.")