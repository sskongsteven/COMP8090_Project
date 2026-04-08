class Notification:
    # Make receipt for each booking to show the details
    def send_booking_receipt(self, user_name, item_name, time_booked):
        print("\n==========================================")
        print("- Booking Receipt:")
        print(f"User: {user_name}")
        print(f"Item: {item_name}")
        print(f"Time: {time_booked}")
        print("Status: Request approved, please directly find the staff for room key/equipment")
        print("==========================================")
