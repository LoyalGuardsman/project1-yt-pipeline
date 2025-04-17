import sys
from pathlib import Path

# required for access to root directory
project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from googleapiclient.discovery import build    # required to create a client for google apis
from config import YOUTUBE_API_KEY, REGIONS, MAX_RESULTS
import pandas as pd
from datetime import datetime, timezone

def fetch_trending_videos(region_code):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    # This accesses the 'videos' endpoint in YT Data API, prepares a .list() request to list videos based on certain filters
    request = youtube.videos().list(  
        part = "snippet, statistics", # snippet: title, channel, publish date, etc. statistics: views, likes, comments
        chart = "mostPopular", # Asks for trending videos, not search results or uploads
        regionCode = region_code,
        maxResults = MAX_RESULTS
    )

    # .execute() sends the HTTP request to Google’s servers, receives a JSON response
    response = request.execute()  # The Google API client parses it into a Python dictionary (from googleapiclient.discovery)
    if "items" not in response:
        raise ValueError("API response is missing list 'items'. Full response:\n" + str(response))
    items = response["items"] # extracts list from API response.

    # Parse data into rows
    videos = []
    for item in items:
        video_data = {
            "video_id": item["id"],
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "published": item["snippet"]["publishedAt"],
            "category": item["snippet"]["categoryId"],
            "region": region_code,
            # .get() is used in case any count is missing (e.g. if likes/comments are turned off)
            # returns 0 if key doesn't exist. Prevents crashes due to KeyError
            "view_count": item["statistics"].get("viewCount", 0),
            "like_count": item["statistics"].get("likeCount", 0),
            "comment_count": item["statistics"].get("commentCount", 0),
            "fetched_at": datetime.now(timezone.utc).isoformat()
        }
        videos.append(video_data)

    return clean_trending_data(pd.DataFrame(videos)) # Converts list of video dicts to table and returns

def clean_trending_data(df):
    # Enforce column order
    df = df[[
        "video_id", "title", "channel", "published",
        "category", "region", "view_count", "like_count",
        "comment_count", "fetched_at"
    ]]

    # Convert columns to proper types
    df["view_count"] = df["view_count"].astype(int)
    df["like_count"] = df["like_count"].astype(int)
    df["comment_count"] = df["comment_count"].astype(int)

    df["published"] = pd.to_datetime(df["published"])
    df["fetched_at"] = pd.to_datetime(df["fetched_at"])

    return df

# test if the code works
if __name__ == "__main__":
    for region in REGIONS:
        print(f"Fetching trending videos for {region}...")
        df = fetch_trending_videos(region)
        print(df.head()) #df.head() prints the first 5 rows of that table
