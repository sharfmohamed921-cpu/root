import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import base64
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configuration
services = ["#New Car ID", "#Renew Car ID", "#New Driving License", "#Renew Driving License", "#Lost ID"]
days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]  # Excluded Friday and Saturday
times = ["9:00AM", "10:00AM", "11:00AM", "12:00PM", "1:00PM"]

# Initialize available slots (max 10 bookings per time slot)
available_slots = {
    service: {
        day: {time: 10 for time in times}
        for day in days
    }
    for service in services
}

# Get dates for the next week (Sunday to Thursday)
def get_week_dates():
    today = datetime.now()
    start_of_week = today + timedelta(days=(6 - today.weekday()))  # Start from next Sunday
    return [f"{days[i]} - {start_of_week + timedelta(days=i):%Y-%m-%d}" for i in range(5)]

# Calculate mean daily reservations for last week from bookings.txt
def calculate_mean():
    last_week = datetime.now() - timedelta(days=7)
    bookings_data = {day: 0 for day in days}
    try:
        with open("bookings.txt", "r", encoding="utf-8") as file:
            for line in file:
                if "Service: #New Car ID" in line:
                    try:
                        booking_date = datetime.strptime(line.split("Booking Date: ")[1].strip(), "%Y-%m-%d %H:%M:%S")
                        if last_week <= booking_date <= datetime.now():
                            day = line.split("Day: ")[1].split(",")[0]
                            if day in bookings_data:
                                bookings_data[day] += 1
                    except (IndexError, ValueError):
                        continue
    except FileNotFoundError:
        pass
    daily_totals = list(bookings_data.values())
    return sum(daily_totals) / len(daily_totals) if daily_totals else 0

# Find most and least crowded days for last week from bookings.txt
def find_most_least_crowded():
    last_week = datetime.now() - timedelta(days=7)
    bookings_data = {day: 0 for day in days}
    try:
        with open("bookings.txt", "r", encoding="utf-8") as file:
            for line in file:
                if "Service: #New Car ID" in line:
                    try:
                        booking_date = datetime.strptime(line.split("Booking Date: ")[1].strip(), "%Y-%m-%d %H:%M:%S")
                        if last_week <= booking_date <= datetime.now():
                            day = line.split("Day: ")[1].split(",")[0]
                            if day in bookings_data:
                                bookings_data[day] += 1
                    except (IndexError, ValueError):
                        continue
    except FileNotFoundError:
        pass
    if not any(bookings_data.values()):
        return "No data", "No data"
    most_crowded = max(bookings_data, key=bookings_data.get)
    least_crowded = min(bookings_data, key=bookings_data.get)
    return most_crowded, least_crowded

# Check password strength
def check_password_strength(password):
    if not password or len(password) != 8 or not password.isalpha() or \
            not any(c.isupper() for c in password) or not any(c.islower() for c in password):
        return "Weak", "#ff4d4d"
    return "Strong", "#2ecc71"

# Encrypt data
def encrypt_data(data):
    return base64.b64encode(data.encode()).decode()

# Decrypt data
def decrypt_data(data):
    try:
        return base64.b64decode(data.encode()).decode()
    except:
        return ""

# Save user data
def save_user(username, password):
    try:
        encrypted_user = encrypt_data(username)
        encrypted_pass = encrypt_data(password)
        with open("users.txt", "a", encoding="utf-8") as file:
            file.write(f"{encrypted_user}:{encrypted_pass}\n")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save user: {e}")

# Check if user exists
def check_user(username, password):
    if not os.path.exists("users.txt"):
        return False
    try:
        with open("users.txt", "r", encoding="utf-8") as file:
            for line in file:
                stored_user, stored_pass = line.strip().split(":")
                if decrypt_data(stored_user) == username and decrypt_data(stored_pass) == password:
                    return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read users: {e}")
        return False
    return False

# Check if username exists
def user_exists(username):
    if not os.path.exists("users.txt"):
        return False
    try:
        with open("users.txt", "r", encoding="utf-8") as file:
            for line in file:
                stored_user, _ = line.strip().split(":")
                if decrypt_data(stored_user) == username:
                    return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to check user existence: {e}")
        return False
    return False

# Save booking
def save_booking(username, full_name, id_number, service, day, time):
    booking_id = f"{username}_{id_number}_{day.split(' - ')[0]}_{time}"
    try:
        with open("bookings.txt", "a", encoding="utf-8") as file:
            file.write(f"BookingID: {booking_id}, Username: {username}, Name: {full_name}, ID: {id_number}, Service: {service}, Day: {day.split(' - ')[0]}, Time: {time}, Booking Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save booking: {e}")

# Check for time conflict
def check_user_time_conflict(username, day, time):
    day_name = day.split(' - ')[0]
    if not os.path.exists("bookings.txt"):
        return False
    try:
        with open("bookings.txt", "r", encoding="utf-8") as file:
            for line in file:
                if f"Username: {username}" in line and f"Day: {day_name}" in line and f"Time: {time}" in line:
                    return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to check time conflict: {e}")
        return False
    return False

# Delete booking
def delete_booking(booking_id, service, day, time):
    try:
        with open("bookings.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
        updated_lines = [line for line in lines if f"BookingID: {booking_id}" not in line]
        with open("bookings.txt", "w", encoding="utf-8") as file:
            file.writelines(updated_lines)
        available_slots[service][day][time] = min(available_slots[service][day][time] + 1, 10)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete booking: {e}")

# Update booking
def update_booking(old_booking_id, username, full_name, id_number, service, day, time):
    delete_booking(old_booking_id, service, day.split(' - ')[0], time)
    save_booking(username, full_name, id_number, service, day, time)

# Count bookings
def count_bookings(service, day, time):
    day_name = day.split(' - ')[0] if ' - ' in day else day
    count = 0
    if not os.path.exists("bookings.txt"):
        return count
    try:
        with open("bookings.txt", "r", encoding="utf-8") as file:
            for line in file:
                if f"Service: {service}" in line and f"Day: {day_name}" in line and f"Time: {time}" in line:
                    count += 1
    except Exception as e:
        messagebox.showerror("Error", f"Failed to count bookings: {e}")
    return count

# Login Window
def login_window():
    login_root = tk.Tk()
    login_root.title("Smart City Booking System")
    login_root.geometry("400x400")
    login_root.configure(bg="#e6f0fa")

    header_frame = tk.Frame(login_root, bg="#4a90e2")
    header_frame.pack(fill="x")
    tk.Label(header_frame, text="Welcome!", font=("Arial", 18, "bold"), bg="#4a90e2", fg="white").pack(pady=10)

    form_frame = tk.Frame(login_root, bg="#e6f0fa")
    form_frame.pack(pady=20)

    tk.Label(form_frame, text="Username:", font=("Arial", 12), bg="#e6f0fa").pack()
    username_entry = ttk.Entry(form_frame, width=25)
    username_entry.pack(pady=5)

    tk.Label(form_frame, text="Password:", font=("Arial", 12), bg="#e6f0fa").pack()
    password_frame = tk.Frame(form_frame, bg="#e6f0fa")
    password_frame.pack(pady=5)
    password_entry = ttk.Entry(password_frame, width=25, show="*")
    password_entry.pack(side="left")

    show_password_var = tk.BooleanVar(value=False)
    show_icon = tk.Button(password_frame, text="👁️", font=("Arial", 12), bg="#e6f0fa", bd=0,
                          command=lambda: toggle_password(show_password_var, password_entry, show_icon))
    show_icon.pack(side="left", padx=5)

    def toggle_password(var, entry, icon):
        if var.get():
            entry.config(show="*")
            icon.config(text="👁️")
        else:
            entry.config(show="")
            icon.config(text="👁️‍🗨️")
        var.set(not var.get())

    def login():
        username = username_entry.get()
        password = password_entry.get()
        if not username or not password:
            messagebox.showwarning("Error", "Please enter username and password")
            return
        if not check_user(username, password):
            messagebox.showwarning("Error", "Invalid username or password")
            return
        messagebox.showinfo("Success", f"Welcome {username}!")
        login_root.destroy()
        booking_window(username)

    def open_register():
        login_root.destroy()
        register_window()

    button_frame = tk.Frame(login_root, bg="#e6f0fa")
    button_frame.pack(pady=20)
    ttk.Button(button_frame, text="Login", command=login, style="Custom.TButton").pack(side="left", padx=10)
    ttk.Button(button_frame, text="Register", command=open_register, style="Custom.TButton").pack(side="left", padx=10)

    login_root.mainloop()

# Register Window
def register_window():
    register_root = tk.Tk()
    register_root.title("Register New Account")
    register_root.geometry("400x450")
    register_root.configure(bg="#e6f0fa")

    header_frame = tk.Frame(register_root, bg="#4a90e2")
    header_frame.pack(fill="x")
    tk.Label(header_frame, text="Create Account", font=("Arial", 18, "bold"), bg="#4a90e2", fg="white").pack(pady=10)

    form_frame = tk.Frame(register_root, bg="#e6f0fa")
    form_frame.pack(pady=20)

    tk.Label(form_frame, text="Username:", font=("Arial", 12), bg="#e6f0fa").pack()
    username_entry = ttk.Entry(form_frame, width=25)
    username_entry.pack(pady=5)

    tk.Label(form_frame, text="Password:", font=("Arial", 12), bg="#e6f0fa").pack()
    password_frame = tk.Frame(form_frame, bg="#e6f0fa")
    password_frame.pack(pady=5)
    password_entry = ttk.Entry(password_frame, width=25, show="*")
    password_entry.pack(side="left")

    show_password_var = tk.BooleanVar(value=False)
    show_icon = tk.Button(password_frame, text="👁️", font=("Arial", 12), bg="#e6f0fa", bd=0,
                          command=lambda: toggle_password(show_password_var, password_entry, show_icon))
    show_icon.pack(side="left", padx=5)

    tk.Label(form_frame, text="Confirm Password:", font=("Arial", 12), bg="#e6f0fa").pack()
    confirm_password_frame = tk.Frame(form_frame, bg="#e6f0fa")
    confirm_password_frame.pack(pady=5)
    confirm_password_entry = ttk.Entry(confirm_password_frame, width=25, show="*")
    confirm_password_entry.pack(side="left")

    show_confirm_var = tk.BooleanVar(value=False)
    show_confirm_icon = tk.Button(confirm_password_frame, text="👁️", font=("Arial", 12), bg="#e6f0fa", bd=0,
                                  command=lambda: toggle_password(show_confirm_var, confirm_password_entry, show_confirm_icon))
    show_confirm_icon.pack(side="left", padx=5)

    strength_label = tk.Label(form_frame, text="Password Strength: Weak", font=("Arial", 10), bg="#e6f0fa", fg="#ff4d4d")
    strength_label.pack(pady=5)

    def update_strength(event):
        password = password_entry.get()
        strength, color = check_password_strength(password)
        strength_label.config(text=f"Password Strength: {strength}", fg=color)

    password_entry.bind("<KeyRelease>", update_strength)

    def toggle_password(var, entry, icon):
        if var.get():
            entry.config(show="*")
            icon.config(text="👁️")
        else:
            entry.config(show="")
            icon.config(text="👁️‍🗨️")
        var.set(not var.get())

    def register():
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        if not username or not password:
            messagebox.showwarning("Error", "Please enter username and password")
            return
        if user_exists(username):
            messagebox.showwarning("Error", "Username already exists!")
            return
        if password != confirm_password:
            messagebox.showwarning("Error", "Passwords do not match")
            return
        strength, _ = check_password_strength(password)
        if strength != "Strong":
            messagebox.showwarning("Error", "Weak Password, please try again. Must be exactly 8 letters with uppercase and lowercase.")
            return
        save_user(username, password)
        messagebox.showinfo("Success", f"Account created successfully! Welcome {username}")
        register_root.destroy()
        booking_window(username)

    def back_to_login():
        register_root.destroy()
        login_window()

    button_frame = tk.Frame(register_root, bg="#e6f0fa")
    button_frame.pack(pady=20)
    ttk.Button(button_frame, text="Create Account", command=register, style="Custom.TButton").pack(side="left", padx=10)
    ttk.Button(button_frame, text="Back", command=back_to_login, style="Custom.TButton").pack(side="left", padx=10)

    register_root.mainloop()

# Booking Window
bookings_window = None
stats_window = None
edit_booking_id = None

def booking_window(username):
    global bookings_window, stats_window, edit_booking_id
    booking_root = tk.Tk()
    booking_root.title("Booking Management")
    booking_root.geometry("600x750")
    booking_root.configure(bg="#e6f0fa")

    header_frame = tk.Frame(booking_root, bg="#4a90e2")
    header_frame.pack(fill="x")
    tk.Label(header_frame, text=f"Welcome {username}!", font=("Arial", 18, "bold"), bg="#4a90e2", fg="white").pack(pady=10)

    form_frame = tk.Frame(booking_root, bg="#e6f0fa")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Full Name:", font=("Arial", 12), bg="#e6f0fa").pack()
    full_name_entry = ttk.Entry(form_frame, width=30)
    full_name_entry.pack(pady=5)

    tk.Label(form_frame, text="ID Number (14 digits):", font=("Arial", 12), bg="#e6f0fa").pack()
    id_entry = ttk.Entry(form_frame, width=30)
    id_entry.pack(pady=5)

    tk.Label(form_frame, text="Select Service:", font=("Arial", 12), bg="#e6f0fa").pack()
    service_combobox = ttk.Combobox(form_frame, values=services, state="readonly", width=27)
    service_combobox.pack(pady=5)
    service_combobox.set(services[0])

    tk.Label(form_frame, text="Select Day:", font=("Arial", 12), bg="#e6f0fa").pack()
    day_combobox = ttk.Combobox(form_frame, values=get_week_dates(), state="readonly", width=27)
    day_combobox.pack(pady=5)
    day_combobox.set(get_week_dates()[0])

    tk.Label(form_frame, text="Select Time:", font=("Arial", 12), bg="#e6f0fa").pack()
    time_combobox = ttk.Combobox(form_frame, values=times, state="readonly", width=27)
    time_combobox.pack(pady=5)
    time_combobox.set(times[0])

    table_frame = tk.Frame(form_frame, bg="#e6f0fa")
    table_frame.pack(pady=10, fill="x")

    table = tk.Frame(table_frame, bg="#e6f0fa", bd=1, relief="solid")
    table.pack(fill="x", padx=10)

    header_frame = tk.Frame(table, bg="#4a90e2")
    header_frame.pack(fill="x")
    tk.Label(header_frame, text="Available Slots", font=("Arial", 12, "bold"), bg="#4a90e2", fg="white").pack(side="left", padx=20)
    tk.Label(header_frame, text="Booked Slots", font=("Arial", 12, "bold"), bg="#4a90e2", fg="white").pack(side="right", padx=20)

    value_frame = tk.Frame(table, bg="white")
    value_frame.pack(fill="x", pady=5)
    available_label = tk.Label(value_frame, text="10", font=("Arial", 12), bg="white", fg="black", width=10)
    available_label.pack(side="left", padx=20)
    booked_label = tk.Label(value_frame, text="0", font=("Arial", 12), bg="white", fg="black", width=10)
    booked_label.pack(side="right", padx=20)

    def update_table(event=None):
        selected_service = service_combobox.get()
        selected_day = day_combobox.get()
        selected_time = time_combobox.get()
        booked = count_bookings(selected_service, selected_day, selected_time)
        available = max(0, 10 - booked)
        available_slots[selected_service][selected_day.split(' - ')[0]][selected_time] = available
        available_label.config(text=str(available))
        booked_label.config(text=str(booked))

    service_combobox.bind("<<ComboboxSelected>>", update_table)
    day_combobox.bind("<<ComboboxSelected>>", update_table)
    time_combobox.bind("<<ComboboxSelected>>", update_table)
    update_table()

    def confirm_booking():
        global edit_booking_id
        full_name = full_name_entry.get()
        id_number = id_entry.get()
        service = service_combobox.get()
        day = day_combobox.get()
        time = time_combobox.get()

        if not full_name or not id_number:
            messagebox.showwarning("Error", "Please enter full name and ID number")
            return
        if not id_number.isdigit() or len(id_number) != 14:
            messagebox.showwarning("Error", "ID number must be 14 digits")
            return
        if check_user_time_conflict(username, day, time) and not edit_booking_id:
            messagebox.showwarning("Error", f"You already have a booking on {day} at {time}")
            return
        if count_bookings(service, day, time) >= 10:
            messagebox.showwarning("Error", f"Booking full for {time} on {day}")
            return

        if edit_booking_id:
            update_booking(edit_booking_id, username, full_name, id_number, service, day, time)
            messagebox.showinfo("Success", f"Booking updated!\nService: {service}\nDay: {day}\nTime: {time}")
            edit_booking_id = None
            confirm_button.config(text="Confirm Booking")
        else:
            available_slots[service][day.split(' - ')[0]][time] -= 1
            save_booking(username, full_name, id_number, service, day, time)
            messagebox.showinfo("Success", f"Booking successful!\nService: {service}\nDay: {day}\nTime: {time}")
        update_table()
        full_name_entry.delete(0, tk.END)
        id_entry.delete(0, tk.END)

    def show_bookings():
        global bookings_window, edit_booking_id
        if bookings_window is not None:
            bookings_window.destroy()

        bookings_window = tk.Toplevel(booking_root)
        bookings_window.title("Your Bookings")
        bookings_window.geometry("600x400")
        bookings_window.configure(bg="#e6f0fa")

        canvas = tk.Canvas(bookings_window, bg="#e6f0fa")
        scrollbar = ttk.Scrollbar(bookings_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#e6f0fa")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        try:
            with open("bookings.txt", "r", encoding="utf-8") as file:
                bookings = file.readlines()
                if not bookings:
                    tk.Label(scrollable_frame, text="No bookings yet!", font=("Arial", 12), bg="#e6f0fa").pack(pady=10)
                else:
                    for booking in bookings:
                        if f"Username: {username}" in booking:
                            booking_id = booking.split(",")[0].split(": ")[1]
                            service = booking.split("Service: ")[1].split(",")[0]
                            day = booking.split("Day: ")[1].split(",")[0]
                            time = booking.split("Time: ")[1].split(",")[0]
                            name = booking.split("Name: ")[1].split(",")[0]
                            id_number = booking.split("ID: ")[1].split(",")[0]

                            booking_frame = tk.Frame(scrollable_frame, bg="#ffffff", bd=2, relief="groove")
                            booking_frame.pack(fill="x", padx=10, pady=5)

                            booking_label = tk.Label(booking_frame, text=booking.strip(), font=("Arial", 10), bg="#ffffff", wraplength=400)
                            booking_label.pack(side="left", padx=10)

                            def confirm_delete(b_id, s, d, t):
                                if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this booking?"):
                                    delete_booking(b_id, s, d, t)
                                    show_bookings()
                                    update_table()

                            def edit_booking(b_id, n, id_num, s, d, t):
                                global edit_booking_id
                                edit_booking_id = b_id
                                full_name_entry.delete(0, tk.END)
                                full_name_entry.insert(0, n)
                                id_entry.delete(0, tk.END)
                                id_entry.insert(0, id_num)
                                service_combobox.set(s)
                                day_combobox.set(f"{d} - {datetime.now().strftime('%Y-%m-%d')}")
                                time_combobox.set(t)
                                confirm_button.config(text="Update Booking")

                            ttk.Button(booking_frame, text="Edit", style="Edit.TButton",
                                       command=lambda b_id=booking_id, n=name, id_num=id_number, s=service, d=day, t=time: edit_booking(b_id, n, id_num, s, d, t)).pack(side="right", padx=5)
                            ttk.Button(booking_frame, text="Delete", style="Delete.TButton",
                                       command=lambda b_id=booking_id, s=service, d=day, t=time: confirm_delete(b_id, s, d, t)).pack(side="right", padx=5)
        except FileNotFoundError:
            tk.Label(scrollable_frame, text="No bookings yet!", font=("Arial", 12), bg="#e6f0fa").pack(pady=10)
        except Exception as e:
            tk.Label(scrollable_frame, text=f"Error loading bookings: {e}", font=("Arial", 12), bg="#e6f0fa").pack(pady=10)

    def show_statistics():
        global stats_window
        if stats_window is not None:
            stats_window.destroy()

        stats_window = tk.Toplevel(booking_root)
        stats_window.title("Booking Statistics")
        stats_window.geometry("800x600")
        stats_window.configure(bg="#e6f0fa")

        header_frame = tk.Frame(stats_window, bg="#4a90e2")
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="Booking Statistics", font=("Arial", 18, "bold"), bg="#4a90e2", fg="white").pack(pady=10)

        table_frame = tk.Frame(stats_window, bg="#e6f0fa")
        table_frame.pack(pady=10, fill="both", expand=True)

        columns = ("Service", "Day", "Time", "Available", "Booked")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        tree.heading("Service", text="Service")
        tree.heading("Day", text="Day")
        tree.heading("Time", text="Time")
        tree.heading("Available", text="Available Slots")
        tree.heading("Booked", text="Booked Slots")
        tree.column("Service", width=120, anchor="center")
        tree.column("Day", width=100, anchor="center")
        tree.column("Time", width=100, anchor="center")
        tree.column("Available", width=100, anchor="center")
        tree.column("Booked", width=100, anchor="center")
        tree.pack(fill="both", expand=True, padx=10)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        for service in services:
            for day in days:
                for time in times:
                    booked = count_bookings(service, day, time)
                    available = max(0, 10 - booked)
                    available_slots[service][day][time] = available
                    tree.insert("", "end", values=(service, day, time, available, booked))

        last_week = datetime.now() - timedelta(days=7)
        bookings_data = {day: 0 for day in days}
        try:
            with open("bookings.txt", "r", encoding="utf-8") as file:
                for line in file:
                    if "Service: #New Car ID" in line:
                        try:
                            booking_date = datetime.strptime(line.split("Booking Date: ")[1].strip(), "%Y-%m-%d %H:%M:%S")
                            if last_week <= booking_date <= datetime.now():
                                day = line.split("Day: ")[1].split(",")[0]
                                if day in bookings_data:
                                    bookings_data[day] += 1
                        except (IndexError, ValueError):
                            continue
        except FileNotFoundError:
            pass

        fig, ax = plt.subplots(figsize=(6, 3))
        ax.bar(bookings_data.keys(), bookings_data.values(), color="#4a90e2")
        ax.set_title("Weekly Bookings for New Car ID")
        ax.set_xlabel("Days")
        ax.set_ylabel("Number of Bookings")

        canvas = FigureCanvasTkAgg(fig, master=stats_window)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

        most_crowded, least_crowded = find_most_least_crowded()
        mean = calculate_mean()
        stats_label = tk.Label(stats_window, text=f"Mean Daily Reservations: {mean:.2f}\nMost Crowded Day: {most_crowded}\nLeast Crowded Day: {least_crowded}",
                               font=("Arial", 12), bg="#e6f0fa", fg="black")
        stats_label.pack(pady=10)

    def logout():
        global bookings_window, stats_window, edit_booking_id
        if bookings_window is not None:
            bookings_window.destroy()
            bookings_window = None
        if stats_window is not None:
            stats_window.destroy()
            stats_window = None
        edit_booking_id = None
        booking_root.destroy()
        login_window()

    button_frame = tk.Frame(booking_root, bg="#e6f0fa")
    button_frame.pack(pady=20)
    confirm_button = ttk.Button(button_frame, text="Confirm Booking", command=confirm_booking, style="Custom.TButton")
    confirm_button.pack(side="left", padx=10)
    ttk.Button(button_frame, text="View Bookings", command=show_bookings, style="Custom.TButton").pack(side="left", padx=10)
    ttk.Button(button_frame, text="Statistics", command=show_statistics, style="Custom.TButton").pack(side="left", padx=10)
    ttk.Button(button_frame, text="Logout", command=logout, style="Custom.TButton").pack(side="left", padx=10)

    style = ttk.Style()
    style.configure("Custom.TButton", font=("Arial", 12), padding=10, background="#4a90e2")
    style.configure("Delete.TButton", font=("Arial", 10), padding=5, background="#ff4d4d")
    style.configure("Edit.TButton", font=("Arial", 10), padding=5, background="#f1c40f")

    booking_root.mainloop()

# Start the system
login_window()