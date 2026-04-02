class User:
    def __init__(self, user_id, name, password):
        self.user_id = user_id
        self.name = name
        # Create private attribute 'password'.
        self.__password = password

    # Check the input password, return the boolean result.
    def verify_password(self, input_password):
        return self.__password == input_password

    # Make sure all subclasses has implemented this basic function.
    def show_menu(self):
        raise NotImplementedError("This method must be implemented in subclasses.")


class Student(User):
    def __init__(self, user_id, name, password):
        super().__init__(user_id, name, password)
        self.role = "Student"

    def show_menu(self):
        print(f"\n--- Student Menu: Welcome, {self.name}! ---")
        print("1. View Available Rooms & Equipment")
        print("2. Make a New Booking")
        print("3. View My Current Bookings")
        print("4. Logout")


class Staff(User):
    def __init__(self, user_id, name, password):
        super().__init__(user_id, name, password)
        self.role = "Staff"

    def show_menu(self):
        print(f"\n--- Staff Menu: Welcome, {self.name}! ---")
        print("1. View All System Bookings")
        print("2. Manage Inventory (Add items)")
        print("3. Process Returns / Release Bookings")
        print("4. Logout")