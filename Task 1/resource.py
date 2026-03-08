class Resource:
    def __init__(self, item_id, name):
        self.item_id = item_id
        self.name = name
        self.is_available = True

    def book_item(self):
        pass


class Equipment(Resource):
    def __init__(self, item_id, name, brand):
        super().__init__(item_id, name)
        self.brand = brand


class Room(Resource):
    def __init__(self, item_id, name, capacity):
        super().__init__(item_id, name)
        self.capacity = capacity
