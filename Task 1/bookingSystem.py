import os
from user import Student, Staff
from resource import Room, Equipment
from utils import Timeutils
from notification import Notification


class BookingSystem:
    def __init__(self):
        self.users = []
        self.resources = []
        self.bookings = []
        self.current_user = None

    # Read data from txt files
    def load_data(self):
        if os.path.exists("Data/users.txt"):
            with open("Data/users.txt", "r") as userData:
                for line in userData:
                    data = line.strip().split(",")
                    # Safety check for the correctness of data
                    if len(data) == 4:
                        role, user_id, name, password = data
                        if role == "Student":
                            self.users.append(Student(user_id, name, password))
                        elif role == "Staff":
                            self.users.append(Staff(user_id, name, password))

        if os.path.exists("Data/resources.txt"):
            with open("Data/resources.txt", "r") as resourceData:
                for line in resourceData:
                    data = line.strip().split(",")
                    # Safety check for the correctness of data
                    if len(data) == 4:
                        resource_type, resource_id, name, extra_info = data
                        if resource_type == "Room":
                            self.resources.append(Room(resource_id, name, int(extra_info)))
                        elif resource_type == "Equipment":
                            self.resources.append(Equipment(resource_id, name, extra_info))

    def save_data(self):
        with open("Data/resources.txt", "w") as resourceData:
            for item in self.resources:
                if hasattr(item, 'capacity'):
                    resourceData.write(f"Room,{item.resource_id},{item.name},{item.capacity}\n")
                else:
                    resourceData.write(f"Equipment,{item.resource_id},{item.name},{item.brand}\n")

    # Process login and store the current user
    def login(self):
        print("--- Welcome to the Booking System ---")
        user_id = input("Enter User ID: ")
        password = input("Enter Password: ")

        for user in self.users:
            if user.user_id == user_id:
                if user.verify_password(password):
                    self.current_user = user
                    print("\nLogin Successful!")
                    return True
                else:
                    print("\nIncorrect password, please try again.")
                    return False

        print("\nUser ID not found.")
        return False

    def view_resources(self):
        print("\n--- Available Rooms & Equipment")
        # If statement to handle accidental case that nothing is found
        if not self.resources:
            print("No resources found in the system.")
            return

        for item in self.resources:
            item.check_info()

    def make_booking(self):
        print("\n--- Make a New Booking ---")
        resource_id = input("Enter the resource ID that you want to make a booking: ")

        for item in self.resources:
            if item.resource_id == resource_id:
                if item.check_availability():
                    item.process_booking()
                    # Record the booking time
                    time_tool = Timeutils()
                    booking_time = time_tool.get_current_time()

                    # Create booking and save it into list of booking record.
                    booking_record = {
                        "user_id": self.current_user.user_id,
                        "resource_id": item.resource_id,
                        "resource_name": item.name,
                        "time": booking_time
                    }
                    self.bookings.append(booking_record)

                    notifier = Notification()
                    notifier.send_booking_receipt(self.current_user.name, item.name, booking_time)

                    print(f"\nYou have successfully booked: {item.name}!")
                    return
                else:
                    print("\nThe item you want to proceed booking is currently not available")
                    return

        print("\nResource ID is invalid, please try again.")

    def view_my_bookings(self):
        print(f"\n--- Current Bookings for {self.current_user.name} ---")
        has_bookings = False

        # Check the booking list and show bookings that fit the current user ID.
        for booking in self.bookings:
            if booking["user_id"] == self.current_user.user_id:
                print(f"- {booking['resource_name']} (ID: {booking['resource_id']})")
                has_bookings = True

        if not has_bookings:
            print("You currently have no active bookings.")

    def view_all_bookings(self):
        print(f"\n--- All System Bookings ---")

        if not self.bookings:
            print("There are currently no active bookings in the system.")
            return

        for booking in self.bookings:
            print(f"\n- User ID: {booking['user_id']}\n- Resource Name: {booking['resource_name']}\n- Resource ID: {booking['resource_id']}")

    def manage_inventory(self):
        print("\n--- Manage Inventory ---")
        print("1. Add a New Room")
        print("2. Add New Equipment")
        print("3. Return to the Main Menu")

        choice = input("\n Please enter the corresponding number to proceed: ")

        # Ask for ID if adding new item
        if choice in ["1","2"]:
            resource_id = input("Please enter the new ID: ")

            # Check if crash with any existing ID
            for item in self.resources:
                if item.resource_id == resource_id:
                    print(f"\nInvalid ID: Already exists, returning to the menu.")
                    return

            if choice == "1":
                name = input("Enter Room Name: ")
                try:
                    capacity = int(input("Enter Room Capacity in Integer: "))
                    self.resources.append(Room(resource_id, name, capacity))
                    self.save_data()
                    print(f"\nThe Room '{name}' has been added to the system.")
                except ValueError:
                    print("\nInvalid capacity, please retry with an integer.")

            elif choice == "2":
                name = input("Enter Equipment Name:")
                eq_type = input("Enter Equipment Brand/Type: ")
                self.resources.append(Equipment(resource_id, name, eq_type))
                self.save_data()
                print(f"\nThe Equipment '{name}' has been added to the system.")

        elif choice == "3":
            print("\nReturning to Main Menu...")
        else:
            print("\nInvalid choice. Returning to Main Menu.")

    def handle_bookings(self):
        if not self.bookings:
            print("\nThere are currently no active bookings to manage.")
            return

        self.view_my_bookings()
        resource_id = input("\nEnter the Resource ID to release/return (enter 'exit' to return): ")

        if resource_id.lower() == 'exit':
            return

        # Locate the position of target item and remove it
        for i, booking in enumerate(self.bookings):
            if booking['resource_id'] == resource_id:
                self.bookings.pop(i)

                for item in self.resources:
                    if item.resource_id == resource_id:
                        item.status = "Available"
                        print(f"\n '{item.name}' has been returned and is now available.")
                        return

        print("\nThere is currently no active booking with the entered ID.")

    def run(self):
        self.load_data()

        while True:
            # Check the login status.
            if self.login():
                while True:
                    # Show menu regarding the login user role
                    self.current_user.show_menu()
                    choice = input("\nPlease enter the corresponding number to proceed: ")

                    if self.current_user.role == "Student":
                        if choice == "1":
                            self.view_resources()
                        elif choice == "2":
                            self.make_booking()
                        elif choice == "3":
                            self.view_my_bookings()
                        elif choice == "4":
                            print("\nLogging out... Goodbye!")
                            self.current_user = None
                            break
                        else:
                            print("\nInvalid choice. Please try again.")

                    elif self.current_user.role == "Staff":
                        if choice == "1":
                            self.view_all_bookings()
                        elif choice == "2":
                            self.manage_inventory()
                        elif choice == "3":
                            self.handle_bookings()
                        elif choice == "4":
                            print("\nLogging out... Goodbye!")
                            self.current_user = None
                            break
                        else:
                            print("\nInvalid choice. Please try again.")

            else:
                print("Returning to login page...")


if __name__ == "__main__":
    booking_system = BookingSystem()
    booking_system.run()
