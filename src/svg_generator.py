"""
SVG Generator module - creates SVG visualizations of current song.
"""
import xml.etree.ElementTree as ET
from datetime import datetime
import base64
import requests
from .config import SVG_WIDTH, SVG_HEIGHT


class SVGGenerator:
    """Generates SVG visualizations of Spotify tracks."""
    
    @staticmethod
    def format_time(milliseconds):
        """Format time from milliseconds to MM:SS format."""
        seconds = int(milliseconds // 1000)
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"
    
    @staticmethod
    def truncate(text, max_length):
        """Truncate text to fit in SVG."""
        if len(text) <= max_length:
            return text
        return text[:max_length - 3] + "..."
    
    @staticmethod
    def get_base64_image(image_url):
        """Download image from URL and convert to base64."""
        try:
            response = requests.get(image_url, timeout=5)
            if response.status_code == 200:
                return base64.b64encode(response.content).decode()
        except Exception as e:
            print(f"Error downloading image: {e}")
        return None
    
    @classmethod
    def create_svg(cls, track):
        """
        Create SVG element for track visualization.
        
        Args:
            track (dict): Track information dictionary
            
        Returns:
            xml.etree.ElementTree.Element: SVG element
        """
        svg = ET.Element("svg", {
            "xmlns": "http://www.w3.org/2000/svg",
            "xmlns:xlink": "http://www.w3.org/1999/xlink",
            "width": str(SVG_WIDTH),
            "height": str(SVG_HEIGHT),
            "viewBox": f"0 0 {SVG_WIDTH} {SVG_HEIGHT}"
        })
        
        # Dark background
        ET.SubElement(svg, "rect", {
            "width": str(SVG_WIDTH),
            "height": str(SVG_HEIGHT),
            "fill": "#1a1a1a",
            "rx": "10"
        })
        
        # Handle no music playing
        if not track:
            ET.SubElement(svg, "text", {
                "x": "50%", "y": "50%",
                "text-anchor": "middle",
                "fill": "white",
                "font-family": "Arial, sans-serif",
                "font-size": "16"
            }).text = "♪ No music playing"
            return svg
        
        # Add album cover on the left
        cls._add_album_cover(svg, track)
        
        # Add track information on the right
        cls._add_track_info(svg, track)
        
        # Add progress bar at the bottom
        cls._add_progress_bar(svg, track)
        
        # Add timer
        cls._add_timer(svg, track)
        
        # Add timestamp
        cls._add_timestamp(svg)
        
        return svg
    
    @staticmethod
    def _add_album_cover(svg, track):
        """Add album cover image to SVG."""
        if not track.get("cover_url"):
            return
        
        # Try to embed the image
        try:
            # Download and convert to base64
            response = requests.get(track["cover_url"], timeout=5)
            if response.status_code == 200:
                import base64
                img_data = base64.b64encode(response.content).decode()
                
                # Add image to SVG on the LEFT
                image_elem = ET.SubElement(svg, "image", {
                    "x": "10",
                    "y": "10",
                    "width": "100",
                    "height": "100",
                    "href": f"data:image/jpeg;base64,{img_data}",
                    "preserveAspectRatio": "xMidYMid slice"
                })
        except Exception as e:
            print(f"Could not add album cover: {e}")
    
    @staticmethod
    def _add_track_info(svg, track):
        """Add song title, artist, and album to SVG on the right."""
        # Title section background
        ET.SubElement(svg, "rect", {
            "x": "120", "y": "10",
            "width": str(SVG_WIDTH - 130),
            "height": "95",
            "fill": "#2a2a2a",
            "rx": "5"
        })
        
        # Header
        ET.SubElement(svg, "text", {
            "x": "130", "y": "28",
            "fill": "#1DB954",
            "font-family": "Arial, sans-serif",
            "font-size": "10",
            "font-weight": "bold"
        }).text = "♪ NOW PLAYING"
        
        # Song name
        song_name = SVGGenerator.truncate(track["name"], 30)
        ET.SubElement(svg, "text", {
            "x": "130", "y": "50",
            "fill": "white",
            "font-size": "15",
            "font-family": "Arial, sans-serif",
            "font-weight": "bold"
        }).text = song_name
        
        # Artist name
        artist_name = SVGGenerator.truncate(track["artist"], 40)
        ET.SubElement(svg, "text", {
            "x": "130", "y": "68",
            "fill": "#B3B3B3",
            "font-size": "11",
            "font-family": "Arial, sans-serif"
        }).text = artist_name
        
        # Album name
        album_name = SVGGenerator.truncate(track["album"], 40)
        ET.SubElement(svg, "text", {
            "x": "130", "y": "83",
            "fill": "#808080",
            "font-size": "9",
            "font-family": "Arial, sans-serif"
        }).text = album_name
    
    @staticmethod
    def _add_progress_bar(svg, track):
        """Add animated progress bar at the bottom."""
        # Container for progress - reduced height
        ET.SubElement(svg, "rect", {
            "x": "10", "y": "115",
            "width": str(SVG_WIDTH - 20),
            "height": "50",
            "fill": "#2a2a2a",
            "rx": "5"
        })
        
        # Calculate progress
        progress_percent = track["progress"] / track["duration"] if track["duration"] else 0
        progress_width = (SVG_WIDTH - 40) * progress_percent
        remaining_time = max((track["duration"] - track["progress"]) / 1000, 0)
        
        # Progress bar background
        ET.SubElement(svg, "rect", {
            "x": "20", "y": "130",
            "width": str(SVG_WIDTH - 40),
            "height": "5",
            "fill": "#404040",
            "rx": "3"
        })
        
        # Animated progress bar
        progress_rect = ET.SubElement(svg, "rect", {
            "x": "20", "y": "130",
            "width": str(progress_width),
            "height": "5",
            "fill": "#1DB954",
            "rx": "3"
        })
        ET.SubElement(progress_rect, "animate", {
            "attributeName": "width",
            "from": str(progress_width),
            "to": str(SVG_WIDTH - 40),
            "dur": f"{remaining_time:.1f}s",
            "fill": "freeze"
        })
    
    @staticmethod
    def _add_timer(svg, track):
        """Add static timer display showing current and total duration."""
        
        # Current time (static)
        timer_y = "160"
        
        # Total duration label
        ET.SubElement(svg, "text", {
            "x": str(SVG_WIDTH - 20), "y": "145",
            "fill": "#808080",
            "font-size": "8",
            "font-family": "Arial, sans-serif",
            "text-anchor": "end"
        }).text = "Duration"
        
        # Total duration (static) - reduced size
        ET.SubElement(svg, "text", {
            "x": str(SVG_WIDTH - 20), "y": timer_y,
            "fill": "white",
            "font-size": "14",
            "font-family": "monospace",
            "font-weight": "bold",
            "text-anchor": "end"
        }).text = SVGGenerator.format_time(track["duration"])
    
    @staticmethod
    def _add_timestamp(svg):
        """Add current timestamp to SVG."""
        ET.SubElement(svg, "text", {
            "x": str(SVG_WIDTH - 20), "y": str(SVG_HEIGHT - 5),
            "fill": "#606060",
            "font-size": "7",
            "text-anchor": "end",
            "font-family": "Arial, sans-serif"
        }).text = datetime.now().strftime("%H:%M:%S")
    
    @staticmethod
    def svg_to_string(svg_element):
        """Convert SVG element to XML string."""
        return ET.tostring(svg_element, encoding="utf-8", method="xml")
