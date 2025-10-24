import json
import os
import pwinput
from Logs.log import error_logs


Userfile = "Database/user.json"

class Signup:

    def __init__(self):
        if not os.path.exists(Userfile):
            with open(Userfile, "w") as file:
                json.dump([], file)


    def createUser(self):
        try:
            username = input("Enter Username: ")
            password = pwinput.pwinput(prompt="Enter Password: ", mask="*")
            role = input("Enter role(admin/staff): ").lower()

            if role not in ["admin","staff"]:
                print("Invalid role ")
                return
             
            with open(Userfile, "r") as file:
                users = json.load(file)

            for user in users:
                if user["username"] == username:
                    print("Username already exists!")
                    return

            users.append({"username": username,
                        "password": password,
                        "role": role})

            with open(Userfile, "w") as file:
                json.dump(users, file, indent=4)

            print(f"{role.capitalize()} '{username}' created successfully.")

        except Exception as e:
            error_logs(e)
