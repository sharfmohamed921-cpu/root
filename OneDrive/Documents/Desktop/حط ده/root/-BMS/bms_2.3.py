from datetime import datetime, timedelta

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
        self.service_data = [new_car_id, renew_car_id, new_driving_license, renew_driving_license, lost_id]

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
        for i, (date, day, slots) in enumerate(service_data, 1):
            print(f"{i}. {day} ({date})")
        print("0. Cancel")
        while True:
            try:
                choice = input("Select day number: ")
                if choice == "0":
                    return None
                choice = int(choice) - 1
                if 0 <= choice < len(service_data):
                    return choice
                print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a number.")

    def select_time(self, service_idx, day_idx):
        if day_idx is None:
            return None
        service_data = self.service_data[service_idx]
        _, _, slots = service_data[day_idx]
        for i, (slot, count) in enumerate(zip(time_slots, slots), 1):
            print(f"{i}. {slot} ({count}/10 bookings)")
        print("0. Cancel")
        while True:
            try:
                choice = input("Select time slot number: ")
                if choice == "0":
                    return None
                choice = int(choice) - 1
                if 0 <= choice < len(time_slots):
                    if slots[choice] >= 10:
                        print("This time slot is fully booked.")
                        return None
                    return choice
                print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a number.")

    def book_appointment(self, service_idx, day_idx, time_idx):
        if any(x is None for x in [service_idx, day_idx, time_idx]):
            return
        service_data = self.service_data[service_idx]
        date, day, slots = service_data[day_idx]
        if slots[time_idx] >= 10:
            print("This time slot is fully booked.")
            return
        full_name = input("Enter your full name: ")
        user_id = input("Enter your ID number (14 digits): ")
        if len(user_id) != 14 or not user_id.isdigit():
            print("ID must be exactly 14 digits. Try again.")
            return
        slots[time_idx] += 1
        booking = f"anonymous,{full_name},{user_id},{services[service_idx]},{day},{time_slots[time_idx]},{date}"
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
                bookings = [line.strip().split(",") for line in f if line.strip()]
                if not bookings:
                    print("No bookings found.")
                    return
                while True:
                    for i, booking in enumerate(bookings, 1):
                        date = datetime.strptime(booking[6], "%d-%m-%Y")
                        is_last_week = date < last_week
                        print(f"{i}. {', '.join(booking)}")
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
                                new_name = input("Enter new name: ")
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

if __name__ == "__main__":
    app = AppointmentSystem()
    while True:
        print("\n1. Book Appointment")
        print("2. Manage Bookings")
        print("3. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            service_idx = app.select_service()
            if service_idx is not None:
                day_idx = app.select_day(service_idx)
                if day_idx is not None:
                    time_idx = app.select_time(service_idx, day_idx)
                    if time_idx is not None:
                        app.book_appointment(service_idx, day_idx, time_idx)
        elif choice == "2":
            app.manage_bookings()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")