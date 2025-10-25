"""
Flask application module - handles HTTP routes and server setup.
"""
from flask import Flask, Response, send_file, send_from_directory
from .spotify_service import SpotifyService
from .svg_generator import SVGGenerator
from .config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG
import os

# Initialize Flask app
app = Flask(__name__, static_folder=os.path.dirname(__file__))

# Initialize Spotify service
spotify_service = SpotifyService()

@app.route("/current-song.svg")
def serve_svg():
    """Serve the current song as an SVG."""
    track = spotify_service.get_current_track(force_update=True)
    svg = SVGGenerator.create_svg(track)
    xml_data = SVGGenerator.svg_to_string(svg)
    
    response = Response(xml_data, mimetype="image/svg+xml")
    
    # Disable cache to force refresh
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response


@app.route("/current-song-refresh.html")
def serve_svg_with_refresh():
    """Serve an HTML page that refreshes the SVG every second."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Now Playing</title>
        <style>
            body { 
                margin: 0; 
                padding: 10px; 
                background-color: #f0f0f0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }
            .container {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            img { 
                max-width: 100%; 
                height: auto;
                display: block;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <img id="svg-image" src="/current-song.svg" alt="Now Playing">
        </div>
        <script>
            // Refresh SVG every second with cache-busting timestamp
            setInterval(function() {
                document.getElementById('svg-image').src = '/current-song.svg?t=' + Date.now();
            }, 1000);
        </script>
    </body>
    </html>
    """
    return html


def run():
    """Run the Flask development server."""
    print("🎵 Current Song SVG Server")
    print("=" * 50)
    print(f"📡 Server starting on http://{FLASK_HOST}:{FLASK_PORT}")
    print("🌐 View the live SVG:")
    print(f"   - http://localhost:{FLASK_PORT}/current-song.svg")
    print(f"   - http://localhost:{FLASK_PORT}/current-song-refresh.html")
    print("=" * 50)
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)


if __name__ == "__main__":
    run()
