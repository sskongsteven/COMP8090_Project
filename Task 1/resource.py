class Resource:
    def __init__(self, resource_id, name):
        self.resource_id = resource_id
        self.name = name
        # Create private attribute 'is_available'.
        self.__is_available = True

    # Check if the resource item is available.
    def check_availability(self):
        return self.__is_available

    # Process the booking request.
    def process_booking(self):
        if self.__is_available:
            self.__is_available = False
            return True
        return False

    # Process the return request.
    def process_return(self):
        self.__is_available = True

    # Function of checking the item information, implement by child class.
    def check_info(self):
        raise NotImplementedError("This method must be implemented in subclasses.")


class Room(Resource):
    def __init__(self, resource_id, name, capacity):
        super().__init__(resource_id, name)
        self.capacity = capacity

    def check_info(self):
        if self.check_availability():
            status = "Available"
        else:
            status = "Borrowed"
        print(f"[Room]\nID: {self.resource_id}\nName: {self.name}\nCapacity: {self.capacity}\nStatus: {status}\n")


class Equipment(Resource):
    def __init__(self, resource_id, name, brand):
        super().__init__(resource_id, name)
        self.brand = brand

    def check_info(self):
        if self.check_availability():
            status = "Available"
        else:
            status = "Borrowed"
        print(f"[Equipment]\nID: {self.resource_id}\nName: {self.name}\nBrand: {self.brand}\nStatus: {status}\n")