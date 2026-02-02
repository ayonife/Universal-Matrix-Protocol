import csv
import os
from datetime import datetime

class BlackBox:
    def __init__(self, filename="matrix_logs.csv"):
        self.filename = filename
        self._initialize_storage()

    def _initialize_storage(self):
        # If file doesn't exist, create it with headers
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["TIMESTAMP", "LOCATION", "LOAD (%)", "DELAY (MIN)", "BURN_RATE (NGN)", "STATUS"])

    def log_event(self, location, congestion, delay_seconds, burn_rate, safety_msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        delay_min = int(delay_seconds / 60)
        congestion_pct = int(congestion * 100)
        
        # Append data to the CSV file
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp, 
                location, 
                f"{congestion_pct}%", 
                delay_min, 
                f"{burn_rate:.2f}", 
                safety_msg
            ])
        return True