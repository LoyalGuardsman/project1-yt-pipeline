import os
from datetime import datetime, timezone
from data_ingestion.fetch_trending import fetch_trending_videos
from config import REGIONS

# Get absolute path to the 'data' directory.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Points to the data folder, located inside the same directory as this script. 
output_dir = os.path.join(BASE_DIR, "data")

timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M")

for region in REGIONS:
    df = fetch_trending_videos(region)

    # Save as CSV
    filename_csv = os.path.join(output_dir, f"trending_{region}_{timestamp}.csv")
    df.to_csv(filename_csv, index=False)

    # Save as JSON
    filename_json = os.path.join(output_dir, f"trending_{region}_{timestamp}.json")
    df.to_json(filename_json, orient="records", lines=True)

    print(f"[{region}] Saved {len(df)} videos to:")
    print(f"  CSV → {filename_csv}")
    print(f"  JSON → {filename_json}")
