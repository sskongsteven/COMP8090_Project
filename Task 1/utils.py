from datetime import datetime


class Timeutils:
    # Get the current time and format it
    def get_current_time(self):
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

