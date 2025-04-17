# utils/helpers.py
import re
from typing import Dict, List, Optional, Union
from PIL import Image

def format_response(text: str) -> str:
    """
    Format agent responses for better readability in Streamlit
    
    Args:
        text (str): Raw text response from agent
        
    Returns:
        str: Formatted text for display
    """
    # Remove any system messages or debug information
    text = re.sub(r'^\s*System:.*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*DEBUG:.*$', '', text, flags=re.MULTILINE)
    
    # Clean up any extra whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()
    
    return text

def check_image_size(image: Image.Image) -> bool:
    """
    Check if image is within optimal size limits
    
    Args:
        image (PIL.Image): Image to check
        
    Returns:
        bool: True if image is within size limits, False otherwise
    """
    MAX_WIDTH = 1600
    MAX_HEIGHT = 1600
    MAX_PIXELS = 1600 * 1600
    
    width, height = image.size
    
    # Check if image is within dimensional limits
    return (width <= MAX_WIDTH and height <= MAX_HEIGHT and (width * height) <= MAX_PIXELS)

def extract_image_metadata(image: Image.Image) -> Dict:
    """
    Extract useful metadata from image
    
    Args:
        image (PIL.Image): Image to analyze
        
    Returns:
        Dict: Dictionary containing image metadata
    """
    metadata = {
        "format": image.format,
        "mode": image.mode,
        "size": image.size,
        "width": image.width,
        "height": image.height
    }
    
    # Try to extract EXIF data if available
    exif_data = {}
    if hasattr(image, '_getexif') and image._getexif():
        exif = image._getexif()
        if exif:
            for tag_id, value in exif.items():
                # Skip binary data
                if isinstance(value, bytes) or isinstance(value, str) and len(value) > 100:
                    continue
                exif_data[tag_id] = str(value)
    
    metadata["exif"] = exif_data if exif_data else None
    
    return metadata

def parse_location_from_response(response: str) -> Optional[str]:
    """
    Extract location information from agent response
    
    Args:
        response (str): Response text to parse
        
    Returns:
        Optional[str]: Extracted location or None
    """
    # Look for location patterns
    location_patterns = [
        r'location:\s*([^\.]+)',
        r'in\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:,\s*[A-Z][a-z]+)*)',
        r'for\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:,\s*[A-Z][a-z]+)*)'
    ]
    
    for pattern in location_patterns:
        match = re.search(pattern, response)
        if match:
            return match.group(1).strip()
    
    return None

def get_issue_severity(response: str) -> Optional[str]:
    """
    Extract severity level from issue detection response
    
    Args:
        response (str): Issue detection response
        
    Returns:
        Optional[str]: Severity level (Low, Medium, High) or None
    """
    severity_pattern = r'severity(?:\s+level)?:\s*(low|medium|high)'
    match = re.search(severity_pattern, response.lower())
    
    if match:
        severity = match.group(1).capitalize()
        return severity
    
    return None