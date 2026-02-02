from datetime import datetime, timedelta
import re
import time

services = [
    'Issue New Car License',
    'Renew Car License',
    'Issue New Driving License',
    'Renew Driving License',
    'Issue Lost ID Replacement'
]

class AppointmentSystem:
    def __init__(self):
        self.logged_in_user = None

    def sanitize_input(self, text):
        return re.sub(r'[,\n\r]', '', text.strip())

    def is_valid_password(self, password):
        warnings = []
        if len(password) != 8:
            warnings.append("Password must be exactly 8 characters long.")
        if not all(c.isalpha() for c in password):
            warnings.append("Password must contain only letters.")
        if not any(c.isupper() for c in password):
            warnings.append("Password must contain at least one uppercase letter.")
        if not any(c.islower() for c in password):
            warnings.append("Password must contain at least one lowercase letter.")
        return warnings, len(warnings) == 0

    def create_account(self):
        while True:
            username = self.sanitize_input(input("Enter new username: "))
            password = input("Enter new password: ")
            confirm_pass = input("Confirm password: ")
            warnings, is_valid = self.is_valid_password(password)
            if warnings:
                for warning in warnings:
                    print(f"Warning: {warning}")
                print("Password conditions: Must be exactly 8 characters long, contain only letters, and include at least one uppercase and one lowercase letter.")
                print("Try again.")
                continue
            if password != confirm_pass:
                print("Passwords do not match. Try again.")
                continue
            try:
                with open("users.txt", "r", encoding="utf-8") as f:
                    users = [line.strip().split(":") for line in f]
                    if any(user[0] == username for user in users):
                        print("Username already exists. Try another.")
                        continue
            except FileNotFoundError:
                pass
            with open("users.txt", "a", encoding="utf-8") as f:
                f.write(f"{username}:{password}\n")
                f.flush()  # Ensure the write is immediately saved
            print("Successful registration!")
            break

    def login(self):
        if self.logged_in_user:
            confirm = input("Already logged in. Confirm login again? (y/n): ").lower()
            if confirm != 'y':
                return self.logged_in_user
        while True:
            username = self.sanitize_input(input("Enter username: "))
            password = input("Enter password: ")
            confirm_pass = input("Confirm password: ")
            _, is_valid = self.is_valid_password(password)
            if not is_valid:
                continue
            if password != confirm_pass:
                print("Passwords do not match. Try again.")
                continue
            try:
                with open("users.txt", "r", encoding="utf-8") as f:
                    users = [line.strip().split(":") for line in f if line.strip()]
                    if not users:
                        print("No users registered. Create an account first.")
                        return None
                    if any(user[0] == username and user[1] == password for user in users):
                        self.logged_in_user = username
                        print(f"Login successful! Welcome, {username}!")
                        return username
                print("Invalid username or password. Create an account first.")
            except FileNotFoundError:
                print("No users registered. Create an account first.")
                return None

    def logout(self):
        if self.logged_in_user:
            confirm = input(f"Logout {self.logged_in_user}? (y/n): ").lower()
            if confirm == 'y':
                self.logged_in_user = None
                print("Logged out successfully!")
            else:
                print("Logout canceled.")
        else:
            print("No user logged in.")

if __name__ == "__main__":
    app = AppointmentSystem()
    app.create_account()
    time.sleep(1)
    app.login()
    if app.logged_in_user:
        app.logout()