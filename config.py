"""
Configuration module for Spotify API credentials and settings.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Spotify API credentials from environment variables (or .env file)
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8080")

# Validate credentials
if not CLIENT_ID or not CLIENT_SECRET:
    print("Error: SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET not found.")
    print("Please create a .env file with your credentials (see .env.example)")
    sys.exit(1)

# Spotify API scope
SPOTIFY_SCOPE = "user-read-currently-playing user-read-playback-state"

# Flask settings
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 8080
FLASK_DEBUG = False

# Cache settings (in seconds)
CACHE_DURATION = 5

# SVG dimensions
SVG_WIDTH = 500
SVG_HEIGHT = 180
