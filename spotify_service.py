"""
Spotify API service module - handles all Spotify API calls and track data.
"""
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SPOTIFY_SCOPE, CACHE_DURATION


class SpotifyService:
    """Service for interacting with Spotify API."""
    
    def __init__(self):
        """Initialize Spotify client with OAuth."""
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                redirect_uri=REDIRECT_URI,
                scope=SPOTIFY_SCOPE
            )
        )
        self.current_track = None
        self.last_update = 0
    
    def get_current_track(self, force_update=False):
        """
        Retrieve current Spotify playback with caching.
        
        Args:
            force_update (bool): Force update even if cache is valid
            
        Returns:
            dict: Track information or None if no track playing
        """
        now = time.time()
        
        # Return cached track if valid
        if not force_update and now - self.last_update < CACHE_DURATION:
            return self.current_track
        
        try:
            playback = self.sp.current_playback()
            self.last_update = now
            
            # Handle case where nothing is playing
            if not playback or not playback.get("item"):
                self.current_track = None
                return None
            
            track = playback["item"]
            
            # Extract track information
            self.current_track = {
                "name": track["name"],
                "artist": ", ".join(a["name"] for a in track["artists"]),
                "album": track["album"]["name"],
                "progress": playback["progress_ms"],
                "duration": track["duration_ms"],
                "is_playing": playback["is_playing"],
                "api_time": now,
                "cover_url": track["album"]["images"][0]["url"] if track["album"]["images"] else None,
            }
            return self.current_track
            
        except Exception as e:
            print(f"Spotify API error: {e}")
            return None
