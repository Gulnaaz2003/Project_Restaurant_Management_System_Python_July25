import json
import os
from Logs.log import error_logs

menuFile = "Database/menu.json"

class MenuManager:

    def __init__(self):
        if not os.path.exists(menuFile):
            os.makedirs(os.path.dirname(menuFile), exist_ok=True)
            with open(menuFile, "w") as f:
                json.dump({
                    "breakfast": [
                        {"id": 1, "name": "Poha", "half_price": 30, "full_price": 50},
                        {"id": 2, "name": "Upma", "half_price": 40, "full_price": 70},
                        {"id": 3, "name": "Tacos", "price": 60},
                        {"id": 4, "name": "Omelete", "price": 30},
                        {"id": 5, "name": "Veg Sandwich", "price": 70},
                        {"id": 6, "name": "Idli Sambhar", "price": 40},
                    ],
                    "lunch": [
                        {"id": 7, "name": "Dal Fry", "half_price": 150, "full_price": 250},
                        {"id": 8, "name": "Aaloo Gobi", "half_price": 120, "full_price": 200},
                        {"id": 9, "name": "Palak Paneer", "half_price": 170, "full_price": 300},
                        {"id": 10, "name": "Chole Bhature", "price": 100},
                        {"id": 11, "name": "Masala Dosa", "price": 160},
                        {"id": 12, "name": "Kaju Carry", "half_price": 160, "full_price": 270},
                        {"id": 13, "name": "Shahi Paneer", "half_price": 180, "full_price": 320},
                        {"id": 14, "name": "Veg Biryani", "half_price": 100, "full_price": 180},
                        {"id": 15, "name": "Dal Makhani", "half_price": 140, "full_price": 250},
                        {"id": 16, "name": "Veg Raita", "half_price": 80, "full_price": 150},
                        {"id": 17, "name": "Tandoori Roti", "price": 12}
                    ],
                    "dinner": [
                        {"id": 18, "name": "Aaloo Matar", "half_price": 110, "full_price": 180},
                        {"id": 19, "name": "Chana Masala", "half_price": 120, "full_price": 200},
                        {"id": 20, "name": "Paneer Pulao", "half_price": 80, "full_price": 170},
                        {"id": 21, "name": "Malai Kofta", "half_price": 170, "full_price": 280},
                        {"id": 22, "name": "Veg Pulao", "half_price": 90, "full_price": 160},
                        {"id": 23, "name": "Butter Naan", "price": 15},
                        {"id": 24, "name": "Tawa Roti", "price": 10},
                        {"id": 25, "name": "Bindi Masala", "half_price": 85, "full_price": 190},
                        {"id": 26, "name": "Besan Gatta", "half_price": 130, "full_price": 220},
                        {"id": 27, "name": "Laccha Paratha", "price": 70},
                        {"id": 28, "name": "Sev Tamatar", "half_price": 110, "full_price": 180},
                        {"id": 29, "name": "Paneer Butter Masala", "half_price": 180, "full_price": 320}
                    ],
                    "drinks": [
                        {"id": 30, "name": "Lassi", "price": 80},
                        {"id": 31, "name": "Cold Coffee", "price": 120},
                        {"id": 32, "name": "Kaju Anjeer Shake", "price": 150},
                        {"id": 33, "name": "Strawberry Shake", "price": 90},
                        {"id": 34, "name": "Mango Juice", "price": 40},
                        {"id": 35, "name": "Hot Coffee", "price": 60}
                    ]
                }, f, indent=4)

    def loadMenu(self):
        with open(menuFile, "r") as file:
            return json.load(file)

    def saveMenu(self, menu):
        with open(menuFile, "w") as file:
            json.dump(menu, file, indent=4)

    def displayMenu(self):
        menu = self.loadMenu()
        print("\n----------- The Sante Food Menu -----------\n")

        for category in ["breakfast", "lunch", "dinner", "drinks"]:
            print(f"==================== {category.capitalize()} ====================")
            if category == "drinks":
                print(f"{'ID':<5}{'Name':<25}{'Half Price':<15}{'Full Price':<15}{'Price':<10}")
                print("-" * 70)
            else:
                print(f"{'ID':<5}{'Name':<25}{'Half Price':<15}{'Full Price':<15}{'Price':<10}")
                print("-" * 70)

            for item in menu.get(category, []):
                id_ = item.get("id", "-")
                name = item.get("name", "-")
                half = f"₹{item.get('half_price')}" if "half_price" in item else "-"
                full = f"₹{item.get('full_price')}" if "full_price" in item else "-"
                price = f"₹{item.get('price')}" if "price" in item else "-"
                print(f"{id_:<5}{name:<25}{half:<15}{full:<15}{price:<10}")
            print()

        # print("------ Admin Menu -------")
        # print("1 - View menu")
        # print("2 - Add menu item")
        # print("3 - Update menu item")
        # print("4 - Delete menu item")
        # print("5 - Exit")

    def addMenuItem(self):
        try:
            menu = self.loadMenu()
            category = input("Enter category (breakfast/lunch/dinner/drinks): ").lower()

            if category not in menu:
                print("Invalid category.")
                return

            new_id = max([item['id'] for cat in menu.values() for item in cat], default=0) + 1
            name = input("Enter item name: ")

            if category == "drinks":
                price = int(input("Enter price: "))
                new_item = {"id": new_id, "name": name, "price": price}
            else:
                half_price = input("Enter half price (leave blank if not applicable): ")
                full_price = input("Enter full price (leave blank if not applicable): ")

                if half_price and full_price:
                    new_item = {"id": new_id, "name": name,
                                "half_price": int(half_price), "full_price": int(full_price)}
                else:
                    price = int(input("Enter single price: "))
                    new_item = {"id": new_id, "name": name, "price": price}

            menu[category].append(new_item)
            self.saveMenu(menu)
            print(f"{name} added successfully to {category} menu!")

        except Exception as e:
            error_logs(e)

    def updateMenuItem(self):
        try:
            menu = self.loadMenu()
            category = input("Enter category (breakfast/lunch/dinner/drinks): ").lower()

            if category not in menu:
                print("Invalid category.")
                return

            self.displayMenu()
            IDtoUpdate = int(input("Enter item ID to update: "))

            for item in menu[category]:
                if item["id"] == IDtoUpdate:
                    print("Leave blank to keep current value.")
                    new_name = input(f"Enter new name ({item['name']}): ") or item['name']
                    item["name"] = new_name

                    if category == "drinks":
                        new_price = input(f"Enter new price ({item['price']}): ")
                        if new_price:
                            item["price"] = int(new_price)
                    else:
                        new_half = input(f"Enter new half price ({item.get('half_price', '-') }): ")
                        new_full = input(f"Enter new full price ({item.get('full_price', '-') }): ")
                        new_price = input(f"Enter new single price ({item.get('price', '-') }): ")

                        if new_half:
                            item["half_price"] = int(new_half)
                        if new_full:
                            item["full_price"] = int(new_full)
                        if new_price:
                            item["price"] = int(new_price)

                    self.saveMenu(menu)
                    print("Item updated successfully!")
                    return
            print("Item not found.")

        except Exception as e:
            error_logs(e)

    def deleteMenuItem(self):
        try:
            menu = self.loadMenu()
            category = input("Enter category (breakfast/lunch/dinner/drinks): ").lower()

            if category not in menu:
                print("Invalid category.")
                return

            self.displayMenu()
            IDtoDelete = int(input("Enter ID to delete: "))
            original_len = len(menu[category])
            menu[category] = [item for item in menu[category] if item["id"] != IDtoDelete]

            if len(menu[category]) < original_len:
                self.saveMenu(menu)
                print("Item deleted successfully!")
            else:
                print("Item not found.")

        except Exception as e:
            error_logs(e)

    def adminMenu(self):
        while True:
            print("\n------ Admin Menu -------")
            print("1 - View menu")
            print("2 - Add menu item")
            print("3 - Update menu item")
            print("4 - Delete menu item")
            print("5 - Exit")

            try:
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    self.displayMenu()
                elif choice == 2:
                    self.addMenuItem()
                elif choice == 3:
                    self.updateMenuItem()
                elif choice == 4:
                    self.deleteMenuItem()
                elif choice == 5:
                    break
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Please enter a valid number.")