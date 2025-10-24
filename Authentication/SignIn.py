from Authentication.SignUp import Signup
from Authentication.UserAuth import Login
from Domain.menu.menucard import MenuManager
from Domain.Order.orderprocessing import OrderManager
from Logs.log import error_logs


def main():
    while True:
        try:
            print("------------- Welcome to The Sante Food --------------")
            print("1. Sign Up")
            print("2. Login")
            print("3. Exit")
            
            choice = input("Choose option: ")

            user = None

            if choice == "1":
                Signup().createUser()
                continue 
            elif choice == "2":
                user = Login().authenticateUser()
                if not user:
                    continue
                print(f"Access granted for {user['role']}")
            elif choice == "3":
                print("Exit...")
                break
            else:
                print("Invalid option.")
                continue

            
            if user["role"] == "admin":
                MenuManager().adminMenu()
            elif user["role"] == "staff":
                OrderManager().staffMenu()
            else:
                print("Unknown role!")

        except Exception as e:
            error_logs(e)