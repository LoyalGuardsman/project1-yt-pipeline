# Simulate a real-time data stream
import os
import schedule
import time
from data_ingestion.fetch_trending import fetch_trending_videos
from config import REGIONS

# Get absolute path to the 'data' directory.
# Translates as 'wherever this script lives — let's treat that folder
# as our base for locating other folders/files nearby'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Points to the data folder, located inside the same directory as this script. 
DATA_DIR = os.path.join(BASE_DIR, "data")

def scheduler():
    for region in REGIONS:
        print(f"Fetching trending videos for {region}...")
        df = fetch_trending_videos(region)
        # Builds the file path where the .csv file will be saved
        file_path = os.path.join(DATA_DIR, f"trending_{region}.csv")
        # Saves the data as a .csv file, excluding row numbers 
        df.to_csv(file_path, index=False)
        print(f"Saved {file_path} with {len(df)} records.")

# Schedule to run every 2 minutes
schedule.every(2).minutes.do(scheduler)

print("Scheduler started. Press CTRL+C to stop.")

while True:
    schedule.run_pending() # Checks whether any scheduled tasks are due to run.
    time.sleep(1) # Waits for 1 second before checking again (to avoid overloading the CPU).