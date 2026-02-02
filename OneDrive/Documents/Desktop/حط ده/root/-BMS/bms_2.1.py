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
        self.service_data = [new_car_id, renew_car_id, new_driving_license, renew_driving_license, lost_id]

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
        print(f"\nAnalyzing bookings:")
        avg_bookings = self.get_average_bookings(0)
        most_crowded, max_bookings = self.get_most_crowded_day(0)
        least_crowded, min_bookings = self.get_least_crowded_day(0)
        print(f"Average daily bookings for {services[0]}: {avg_bookings:.1f}")
        print(f"Most crowded day for {services[0]}: {most_crowded} with {max_bookings} bookings")
        print(f"Least crowded day for {services[0]}: {least_crowded} with {min_bookings} bookings")

if __name__ == "__main__":
    app = AppointmentSystem()
    app.analyze_bookings()