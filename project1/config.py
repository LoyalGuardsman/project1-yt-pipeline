from dotenv import load_dotenv
import os

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
REGIONS = os.getenv("REGIONS").split(",")  # Converts comma-separated string to list
MAX_RESULTS = int(os.getenv("MAX_RESULTS"))