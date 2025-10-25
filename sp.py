#!/usr/bin/env python3
"""
Current Song SVG Generator - Main entry point.

This application displays the currently playing Spotify song as an SVG visualization
with real-time animated progress bar and timer.

Usage:
    export SPOTIFY_CLIENT_ID="your_client_id"
    export SPOTIFY_CLIENT_SECRET="your_client_secret"
    python sp.py
"""

from app import run

if __name__ == "__main__":
    run()
