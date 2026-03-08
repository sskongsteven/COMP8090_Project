class User:
    def __init__(self, user_id, name, password):
        self.user_id = user_id
        self.name = name
        self.password = password

    def verify_password(self, input_password):
        return self.password == input_password

    def show_menu(self):
        pass


class Student(User):
    def show_menu(self):
        print("1. Search Equipment")
        print("2. My Bookings")


class Staff(User):
    def show_menu(self):
        print("1. Manage Inventory")
        print("2. View All Bookings")