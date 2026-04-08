import tkinter as tk
from tkinter import messagebox
from bookingSystem import BookingSystem, Room, Equipment
from utils import Timeutils
from notification import Notification


class BookingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Booking System")
        self.root.geometry("400x300")

        # Get data and functions from the backend
        self.system = BookingSystem()
        self.system.load_data()
        self.create_login_screen()

    def create_login_screen(self):
        # Create Title
        title = tk.Label(self.root, text="Welcome to the Booking System", font=("Arial", 14, "bold"))
        title.pack(pady=20)

        # Create User ID input
        tk.Label(self.root, text="User ID:").pack()
        self.entry_user = tk.Entry(self.root)
        self.entry_user.pack(pady=5)

        # Create password input
        tk.Label(self.root, text="Password:").pack()
        self.entry_password = tk.Entry(self.root)
        self.entry_password.pack(pady=5)

        # Create Login Button
        login_btn = tk.Button(self.root, text="Login", command=self.attempt_login)
        login_btn.pack(pady=20)

    def attempt_login(self):
        user_id = self.entry_user.get()
        password = self.entry_password.get()

        user_found = False
        for user in self.system.users:
            if user.user_id == user_id:
                user_found = True
                if user.verify_password(password):
                    self.system.current_user = user
                    messagebox.showinfo("Success", f"Welcome, {user.name}!")

                    # Remove the login screen to move on
                    self.clear_window()

                    if user.role == "Student":
                        self.show_student_menu()
                    elif user.role == "Staff":
                        self.show_staff_menu()
                    return
                else:
                    messagebox.showerror("Error", "Incorrect password")
                    return

        if not user_found:
            messagebox.showerror("Error", "User ID not found.")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_student_menu(self):
        tk.Label(self.root, text=f"Student Menu: {self.system.current_user.name}", font=("Arial", 14, "bold")).pack(pady=20)

        tk.Button(self.root, text="1. View Available Resources", width=30, command=self.view_resources_gui).pack(pady=5)
        tk.Button(self.root, text="2. Make a New Booking", width=30, command=self.make_booking_gui).pack(pady=5)
        tk.Button(self.root, text="3. View My Current Bookings", width=30, command=self.view_bookings_gui).pack(pady=5)

        tk.Button(self.root, text="Logout", width=30, fg="red", command=self.logout).pack(pady=20)

    def show_staff_menu(self):
        tk.Label(self.root, text=f"Staff Menu: {self.system.current_user.name}", font=("Arial", 14, "bold")).pack(pady=20)

        tk.Button(self.root, text="1. View All System Booking", width=30, command=self.view_all_bookings_gui).pack(pady=5)
        tk.Button(self.root, text="2. Manage Inventory (Add Items)", width=30, command=self.manage_inventory_gui).pack(pady=5)
        tk.Button(self.root, text="3. Process Returns", width=30, command=self.process_returns_gui).pack(pady=5)

        tk.Button(self.root, text="Logout", width=30, fg="red", command=self.logout).pack(pady=20)

    def logout(self):
        self.system.current_user = None
        self.clear_window()
        self.create_login_screen()

    def coming_soon(self):
        messagebox.showinfo("Info", "coming soon.")

    def view_resources_gui(self):
        popup = tk.Toplevel(self.root)
        popup.title("Available Resources")
        popup.geometry("350x400")

        text_box = tk.Text(popup, wrap="word", font=("Arial", 10))
        text_box.pack(expand=True, fill="both", padx=10, pady=10)

        display_text = "--- Available Rooms & Equipments ---\n\n"

        if not self.system.resources:
            display_text += "No resources found in the system."
        else:
            for item in self.system.resources:
                status = "Available" if item.check_availability() else "Borrowed"

                # Check if the item is a room
                if hasattr(item, 'capacity'):
                    display_text += f"[Room]\nID: {item.resource_id}\nName: {item.name}\nCapacity: {item.capacity}\nStatus: {status}\n\n"
                else:
                    display_text += f"[Equipment]\nID: {item.resource_id}\nName: {item.name}\nBrand/Type: {item.brand}\nStatus: {status}\n\n"

        text_box.insert("1.0", display_text)
        text_box.config(state="disabled")

    def view_bookings_gui(self):
        popup = tk.Toplevel(self.root)
        popup.title("My Current Bookings")
        popup.geometry("350x400")

        text_box = tk.Text(popup, wrap="word", font=("Arial", 10))
        text_box.pack(expand=True, fill="both", padx=10, pady=10)

        display_text = "--- My Bookings ---\n\n"

        # Loop through the booking list and store the booking with the correct user id
        user_bookings = []
        for booking in self.system.bookings:
            if booking["user_id"] == self.system.current_user.user_id:
                user_bookings.append(booking)

        if not user_bookings:
            display_text += "You have no current bookings."
        else:
            for b in user_bookings:
                display_text += f"\nItem: {b['resource_name']}\nResource ID: {b['resource_id']}\nTime Booked: {b.get('time', 'N/A')}\n"

        text_box.insert("1.0", display_text)
        text_box.config(state="disabled")

    def make_booking_gui(self):
        popup = tk.Toplevel(self.root)
        popup.title("Make a Booking")
        popup.geometry("300x150")

        tk.Label(popup, text="Enter Resource ID to Book:").pack(pady=10)
        entry_resource = tk.Entry(popup)
        entry_resource.pack(pady=5)

        def submit_booking():
            res_id = entry_resource.get()

            resource_to_book = None
            for item in self.system.resources:
                if item.resource_id == res_id:
                    resource_to_book = item
                    break

            # Error checking
            if not resource_to_book:
                messagebox.showerror("Error", "Resource ID not found.", parent=popup)
                return
            if not resource_to_book.check_availability():
                messagebox.showerror("Error", "This item is currently borrowed.", parent=popup)
                return

            resource_to_book.process_booking()

            time_tool = Timeutils()
            booking_time = time_tool.get_current_time()

            # Add the booking record
            booking_record = {
                "user_id": self.system.current_user.user_id,
                "resource_id": resource_to_book.resource_id,
                "resource_name": resource_to_book.name,
                "time": booking_time
            }
            self.system.bookings.append(booking_record)

            notifier = Notification()
            notifier.send_booking_receipt(self.system.current_user.name, resource_to_book.name, booking_time)

            messagebox.showinfo("Success", f"Successfully booked: {resource_to_book.name}!", parent=popup)
            popup.destroy()

        tk.Button(popup, text="Book Now", command=submit_booking).pack(pady=10)

    def view_all_bookings_gui(self):
        popup = tk.Toplevel(self.root)
        popup.title("All System Bookings")
        popup.geometry("400x400")

        text_box = tk.Text(popup, wrap="word", font=("Arial", 10))
        text_box.pack(expand=True, fill="both", padx=10, pady=10)

        display_text = "--- All Active Bookings ---\n\n"

        if not self.system.bookings:
            display_text += "There are no active bookings in the system."
        else:
            for b in self.system.bookings:
                display_text += f"\nUser ID: {b['user_id']}\nResource: {b['resource_name']} (ID: {b['resource_id']})\nTime: {b.get('time', 'N/A')}\n"

        text_box.insert("1.0", display_text)
        text_box.config(state="disabled")

    def process_returns_gui(self):
        popup = tk.Toplevel(self.root)
        popup.title("Process Return")
        popup.geometry("300x150")

        tk.Label(popup, text="Enter Resource ID to Return:").pack(pady=10)
        entry_resource = tk.Entry(popup)
        entry_resource.pack(pady=5)

        def submit_return():
            res_id = entry_resource.get()

            resource_to_return = None
            for item in self.system.resources:
                if item.resource_id == res_id:
                    resource_to_return = item
                    break

            if not resource_to_return:
                messagebox.showerror("Error", "Resource ID not found.", parent=popup)
                return
            if resource_to_return.check_availability():
                messagebox.showerror("Error", "This item is already available.")
                return

            resource_to_return.process_return()

            for booking in self.system.bookings:
                if booking["resource_id"] == res_id:
                    self.system.bookings.remove(booking)
                    break

            messagebox.showinfo("Success", f"Successfully returned: {resource_to_return.name}!", parent=popup)
            popup.destroy()

        tk.Button(popup, text="Confirm Return", command=submit_return).pack(pady=10)

    def manage_inventory_gui(self):
        popup = tk.Toplevel(self.root)
        popup.title("All New Resource")
        popup.geometry("300x350")

        # Let user to select room or equipment
        tk.Label(popup, text="Select Item Type:").pack(pady=5)
        type_var = tk.StringVar(value="Room")
        tk.Radiobutton(popup, text="Room", variable=type_var, value="Room").pack()
        tk.Radiobutton(popup, text="Equipment", variable=type_var, value="Equipment").pack()

        # Input text field
        tk.Label(popup, text="Resource ID:").pack(pady=5)
        entry_id = tk.Entry(popup)
        entry_id.pack()

        tk.Label(popup, text="Name:").pack(pady=5)
        entry_name = tk.Entry(popup)
        entry_name.pack()

        tk.Label(popup, text="Capacity (for Room) / Brand (for Equipment)").pack(pady=5)
        entry_extra = tk.Entry(popup)
        entry_extra.pack()

        def submit_item():
            res_type = type_var.get()
            res_id = entry_id.get()
            name = entry_name.get()
            extra = entry_extra.get()

            # Check if all information are filled
            if not res_id or not name or not extra:
                messagebox.showerror("Error", "Please fill in all fields.", parent=popup)
                return

            for item in self.system.resources:
                if item.resource_id == res_id:
                    messagebox.showerror("Error", "This ID already exists in the system.", parent=popup)
                    return

            if res_type == "Room":
                new_item = Room(res_id, name, extra)
            else:
                new_item = Equipment(res_id, name, extra)

            self.system.resources.append(new_item)
            self.system.save_data()

            messagebox.showinfo("Success", f"Successfully added {res_type}: {name}!", parent=popup)
            popup.destroy()

        tk.Button(popup, text="Add to System", command=submit_item).pack(pady=20)


if __name__ == "__main__":
    window = tk.Tk()
    app = BookingGUI(window)
    window.mainloop()