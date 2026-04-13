class WaitingListNode:
    # Represents Task 1 Users in the waitlist.
    def __init__(self, name, role, request_time):
        self.name = name
        self.role = role
        self.request_time = request_time
        # Staff has a higher priority than student
        self.priority = 2 if self.role == "Staff" else 1

    def __repr__(self):
        return f"[{self.role}] {self.name} (Priority: {self.priority})"


class PriorityWaitlist:
    # The Max-Heap Data Structure for the priority waitlist.
    def __init__(self):
        self.heap = []

    def parent(self, i):
        return (i - 1) // 2

    def left_child(self, i):
        return 2 * i + 1

    def right_child(self, i):
        return 2 * i + 2

    # Add the user into the waitlist
    def insert(self, node):
        self.heap.append(node)
        current = len(self.heap) - 1

        # When current node has a higher priority than the parent up, swap them and continue
        while current > 0 and self.heap[current].priority > self.heap[self.parent(current)].priority:
            parent_idx = self.parent(current)
            self.heap[current], self.heap[parent_idx] = self.heap[parent_idx], self.heap[current]
            current = parent_idx

    # Removes and returns the user with the highest priority
    def extract_max(self):
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]

        # Remove the last element and move it to the root, then bubble down it to restore Max-Heap
        self.heap[0] = self.heap.pop()

        self.heapify_down(0)

        return root

    # Continuously bubble down the element base on priority
    def heapify_down(self, i):
        largest = i
        left = self.left_child(i)
        right = self.right_child(i)
        n = len(self.heap)

        if left < n and self.heap[left].priority >self.heap[largest].priority:
            largest = left

        if right < n and self.heap[right].priority >self.heap[largest].priority:
            largest = right

        if largest != i:
            self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
            self.heapify_down(largest)


# Heapify function to sort rooms by capacity
def heapify_for_sort(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left]['capacity'] > arr[largest]['capacity']:
        largest = left

    if right < n and arr[right]['capacity'] >arr[largest]['capacity']:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify_for_sort(arr, n, largest)

# Repeatedly call the heapify function to sort the array in ascending order
def heap_sort_rooms(arr):
    n = len(arr)

    # First make a Max-Heap to make sure the largest node is at the index 0
    for i in range(n // 2 - 1, -1, -1):
        heapify_for_sort(arr, n, i)

    # Put the largest at the end, reduce length by one and continue until it is fully sorted
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify_for_sort(arr, i, 0)



# Test Case
if __name__ == "__main__":
    # Keep inserting the members into the list and print the list, it should already placed the higher priority at the top
    print("======= Part 1 Demo: Priority Waitlist (Data Structure: Heap) =======\n")
    waitlist = PriorityWaitlist()

    waitlist.insert(WaitingListNode("Alice", "Student", "10:00 AM"))
    waitlist.insert(WaitingListNode("Ben", "Student", "10:05 AM"))

    waitlist.insert(WaitingListNode("Dr.Smith", "Staff", "10:30 AM"))

    print("Waitlist status:", waitlist.heap)

    # Use the extract function to allocate rooms to members.
    print("\nProcessing Waitlist by allocating to higher priority first:")
    print("1st Room Given to:", waitlist.extract_max())
    print("2nd Room Given to:", waitlist.extract_max())
    print("3rd Room Given to:", waitlist.extract_max())



    print("\n\n======= Part 2 Demo: Room Sorting (Algorithm: Heap Sort) =======")
    rooms = [
        {"id": "R101", "name": "Conference Room A", "capacity": 20},
        {"id": "R302", "name": "Study Room B", "capacity": 4},
        {"id": "R001", "name": "Hall", "capacity": 300},
        {"id": "R104", "name": "Classroom 1C", "capacity": 40},
        {"id": "R105", "name": "Classroom 1D", "capacity": 40},
        {"id": "R106", "name": "Classroom 1E", "capacity": 30}
    ]

    # Show original list of rooms
    print("Before Sorting:")
    for room in rooms: print(room)

    heap_sort_rooms(rooms)

    # Sort it and print the result in ascending order
    print("\nAfter Sorting (By ascending order):")
    for room in rooms: print(room)
