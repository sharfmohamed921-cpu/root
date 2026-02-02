from datetime import datetime, timedelta
import re

services = [
    'Issue New Car License',
    'Renew Car License',
    'Issue New Driving License',
    'Renew Driving License',
    'Issue Lost ID Replacement'
]

new_car_id = [
    ["13-04-2025", "Sunday", [4, 6, 7, 8, 1]],
    ["14-04-2025", "Monday", [2, 1, 8, 6, 4]],
    ["15-04-2025", "Tuesday", [3, 1, 6, 6, 4]],
    ["16-04-2025", "Wednesday", [1, 6, 9, 8, 3]],
    ["17-04-2025", "Thursday", [4, 7, 7, 10, 1]]
]

renew_car_id = [
    ["13-04-2025", "Sunday", [4, 9, 7, 7, 1]],
    ["14-04-2025", "Monday", [3, 1, 7, 7, 3]],
    ["15-04-2025", "Tuesday", [3, 5, 9, 10, 2]],
    ["16-04-2025", "Wednesday", [3, 6, 6, 9, 1]],
    ["17-04-2025", "Thursday", [1, 2, 9, 8, 4]]
]

new_driving_license = [
    ["13-04-2025", "Sunday", [2, 4, 9, 6, 2]],
    ["14-04-2025", "Monday", [2, 6, 8, 8, 1]],
    ["15-04-2025", "Tuesday", [4, 5, 6, 8, 2]],
    ["16-04-2025", "Wednesday", [3, 10, 6, 10, 1]],
    ["17-04-2025", "Thursday", [2, 5, 10, 6, 2]]
]

renew_driving_license = [
    ["13-04-2025", "Sunday", [2, 6, 10, 8, 4]],
    ["14-04-2025", "Monday", [1, 3, 7, 7, 4]],
    ["15-04-2025", "Tuesday", [2, 6, 10, 6, 1]],
    ["16-04-2025", "Wednesday", [2, 10, 7, 8, 1]],
    ["17-04-2025", "Thursday", [2, 7, 7, 7, 1]]
]

lost_id = [
    ["13-04-2025", "Sunday", [1, 3, 9, 8, 3]],
    ["14-04-2025", "Monday", [3, 9, 6, 6, 4]],
    ["15-04-2025", "Tuesday", [4, 7, 8, 7, 3]],
    ["16-04-2025", "Wednesday", [3, 9, 6, 9, 4]],
    ["17-04-2025", "Thursday", [2, 4, 10, 7, 1]]
]

time_slots = ["9:00AM", "10:00AM", "11:00AM", "12:00PM", "1:00PM"]
days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
class AppointmentSystem:
    def __init__(self):
        self.logged_in_user = None
        self.service_data = [new_car_id, renew_car_id, new_driving_license, renew_driving_license, lost_id]

    def sanitize_input(self, text):
        return re.sub(r'[,\n\r]', '', text.strip())

    def is_valid_password(self, password):
        if len(password) != 8:
            return False, "Password must be exactly 8 characters long."
        if not all(c.isalpha() for c in password):
            return False, "Password must contain only letters."
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter."
        if not any(c.islower() for c in password):

            return False, "Password must contain at least one lowercase letter."
        return True, ""

    def login(self):
        if self.logged_in_user:
            confirm = input("Already logged in. Confirm login again? (y/n): ").lower()
            if confirm != 'y':
                return self.logged_in_user
        while True:
            username = self.sanitize_input(input("Enter username: "))
            password = input("Enter password: ")
            confirm_pass = input("Confirm password: ")

            is_valid, error = self.is_valid_password(password)

            if not is_valid:
                print(error)
                continue
            if password != confirm_pass:
                print("Passwords do not match. Try again.")
                continue

            try:
                with open("users.txt", "r", encoding="utf-8") as f:
                    users = [line.strip().split(":") for line in f]
                    if any(user[0] == username and user[1] == password for user in users):
                        self.logged_in_user = username
                        print(f"Login successful! Welcome, {username}!")
                        return username
                print("Invalid username or password. Create an account first.")
            except FileNotFoundError:
                print("No users registered. Create an account first.")

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

    def create_account(self):
        while True:

            username = self.sanitize_input(input("Enter new username: "))
            password = input("Enter new password: ")

            confirm_pass = input("Confirm password: ")

            is_valid, error = self.is_valid_password(password)
            if not is_valid:
                print(error)
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
            print("Account created successfully!")
            break

    def select_service(self):
        for i, service in enumerate(services, 1):
            print(f"{i}. {service}")
        print("0. Cancel")

        while True:
            try:
                choice = input("Select service number (0-5): ")
                if choice == "0":
                    return None
                choice = int(choice) - 1
                if 0 <= choice < len(services):
                    return choice
                print("Invalid choice. Try again.")
            except ValueError:


                print("Please enter a number.")

    def select_day(self, service_idx):
        if service_idx is None:
            return None
        service_data = self.service_data[service_idx]
        available_days = [i for i, entry in enumerate(service_data) if any(count < 10 for count in entry[2])]
        if not available_days:
            print("No available days for this service.")
            return None
        for i, idx in enumerate(available_days, 1):
            print(f"{i}. {service_data[idx][1]} ({service_data[idx][0]})")
        print("0. Cancel")
        while True:
            try:

                choice = input("Select day number: ")
                if choice == "0":
                    return None
                choice = int(choice) - 1
                if 0 <= choice < len(available_days):

                    return available_days[choice]
                print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a number.")

    def select_time(self, service_idx, day_idx):
        if day_idx is None:


            return None
        service_data = self.service_data[service_idx]
        _, _, slots = service_data[day_idx]
        available_times = [i for i, count in enumerate(slots) if count < 10]
        if not available_times:
            print("No available time slots for this day.")
            return None



        for i, idx in enumerate(available_times, 1):
            print(f"{i}. {time_slots[idx]} ({slots[idx]}/10 bookings)")
        print("0. Cancel")
        while True:

            try:
                choice = input("Select time slot number: ")
                if choice == "0":
                    return None
                choice = int(choice) - 1
                if 0 <= choice < len(available_times):
                    return available_times[choice]
                print("Invalid choice. Try again.")
            except ValueError:

                print("Please enter a number.")

    def book_appointment(self, service_idx, day_idx, time_idx):
        if any(x is None for x in [service_idx, day_idx, time_idx]):
            return
        service_data = self.service_data[service_idx]
        date, day, slots = service_data[day_idx]
        if slots[time_idx] >= 10:
            print("Time slot is fully booked.")
            return
        full_name = self.sanitize_input(input("Enter your full name: "))
        user_id = input("Enter your ID number (14 digits): ")
        if len(user_id) != 14 or not user_id.isdigit():
            print("ID must be exactly 14 digits. Try again.")
            return
        slots[time_idx] += 1
        booking = f"{self.logged_in_user},{full_name},{user_id},{services[service_idx]},{day},{time_slots[time_idx]},{date}"
        try:
            with open("bookings.txt", "a", encoding="utf-8") as f:
                f.write(booking + "\n")
            print(f"Booking Confirmed!\n{booking}")
        except Exception as e:
            print(f"Error saving booking: {e}")

    def manage_bookings(self):
        current_date = datetime.now()
        last_week = current_date - timedelta(days=7)
        try:
            with open("bookings.txt", "r", encoding="utf-8") as f:
                bookings = [line.strip().split(",") for line in f if line.strip().startswith(self.logged_in_user + ",")]
                if not bookings:
                    print("No bookings found for this user.")
                    return
                while True:
                    for i in range(len(bookings)):
                        booking = bookings[i]
                        date = datetime.strptime(booking[6], "%d-%m-%Y")
                        is_last_week = date < last_week
                        print(f"{i+1}. {', '.join(booking)}")
                    print(f"Action - 1: Delete, 2: {'Edit' if is_last_week else 'N/A'}, 0: Exit")
                    action = input("Choose action: ")
                    if action == "0":
                        break
                    try:
                        choice = int(action) - 1
                        if 0 <= choice < len(bookings):
                            booking = bookings[choice]
                            if action == "1":
                                bookings.pop(choice)
                                with open("bookings.txt", "w", encoding="utf-8") as f:
                                    for b in bookings:
                                        f.write(",".join(b) + "\n")
                                print("Booking deleted.")
                            elif action == "2" and is_last_week:
                                new_name = self.sanitize_input(input("Enter new name: "))
                                new_id = input("Enter new ID (14 digits): ")
                                if len(new_id) != 14 or not new_id.isdigit():
                                    print("ID must be exactly 14 digits. Try again.")
                                    continue
                                booking[1] = new_name
                                booking[2] = new_id
                                with open("bookings.txt", "w", encoding="utf-8") as f:
                                    for b in bookings:
                                        f.write(",".join(b) + "\n")
                                print("Booking updated.")
                            else:
                                print("Invalid action or not editable.")
                        else:
                            print("Invalid choice. Try again.")
                    except ValueError:
                        print("Please enter a number.")
        except FileNotFoundError:
            print("No bookings file found.")
        except Exception as e:
            print(f"Error managing bookings: {e}")

    def get_average_bookings(self, service_idx):
        service_data = self.service_data[service_idx]
        total_bookings = [sum(day[2]) for day in service_data]
        return sum(total_bookings) / len(total_bookings) if total_bookings else 0

    def get_most_crowded_day(self, service_idx):
        service_data = self.service_data[service_idx]
        total_bookings = [sum(day[2]) for day in service_data]
        max_index = total_bookings.index(max(total_bookings))
        return service_data[max_index][1], max(total_bookings)

    def get_least_crowded_day(self, service_idx):
        service_data = self.service_data[service_idx]
        total_bookings = [sum(day[2]) for day in service_data]
        min_index = total_bookings.index(min(total_bookings))
        return service_data[min_index][1], min(total_bookings)

    def analyze_bookings(self):
        if not self.logged_in_user:
            print("Please log in to analyze bookings.")
            return
        print(f"\nAnalyzing bookings for {self.logged_in_user}:")
        avg_bookings = self.get_average_bookings(0)

        most_crowded, max_bookings = self.get_most_crowded_day(0)
        least_crowded, min_bookings = self.get_least_crowded_day(0)
        print(f"Average daily bookings for {services[0]}: {avg_bookings:.1f}")
        print(f"Most crowded day for {services[0]}: {most_crowded} with {max_bookings} bookings")
        print(f"Least crowded day for {services[0]}: {least_crowded} with {min_bookings} bookings")


if __name__ == "__main__":
    app = AppointmentSystem()
    while True:
        if not app.logged_in_user:
            print("\n1. Create Account")
            print("2. Login")
            print("5. Exit")
        else:
            print(f"\nLogged in as: {app.logged_in_user}")
            print("1. Create Account")
            print("3. Book Appointment")
            print("4. Manage Bookings")
            print("7. Analyze Bookings")
            print("6. Logout")
            print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            app.create_account()
        elif choice == "2" and not app.logged_in_user:
            app.login()
        elif choice == "3" and app.logged_in_user:
            service_idx = app.select_service()
            day_idx = app.select_day(service_idx)
            if day_idx is not None:
                time_idx = app.select_time(service_idx, day_idx)
                if time_idx is not None:
                    app.book_appointment(service_idx, day_idx, time_idx)
        elif choice == "4" and app.logged_in_user:
            app.manage_bookings()
        elif choice == "7" and app.logged_in_user:
            app.analyze_bookings()
        elif choice == "6" and app.logged_in_user:
            app.logout()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice or action not available. Try again.")