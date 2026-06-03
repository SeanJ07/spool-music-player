#!/usr/bin/env python3
"""
Create a simple vinyl record icon for Spool using Python.
Generates a 256x256 PNG icon with vinyl disc appearance.
"""

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("❌ PIL (Pillow) not available. Creating simple placeholder...")
    # Create a simple placeholder using a tiny PNG
    import base64
    
    # Small blank PNG as fallback
    blank_png = base64.b64decode("""
    iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlz
    AAAB2AAAAdgB+lymcgAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjZyBAZWFya2luZy4AZWRhLzEy
    OTQvaW4vDwEAUHJpbnRlZCBhbmQgZW5jb2RlZCBieSBHb2xsZWF0IENvbXBvc2l0ZSBtYWtlciAyMDIy
    L0JvYXRtYW4gS2FuZyAoMSkAAABJRU5ErkJggg==
    """)
    
    with open('assets/spool-icon.png', 'wb') as f:
        f.write(blank_png)
    
    print("📁 Created placeholder icon")
    exit()

def create_vinyl_icon():
    """Create a vinyl record icon with Spool branding."""
    
    # Create 256x256 image
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    center = size // 2
    
    # Dark vinyl disc
    vinyl_color = (26, 15, 8, 255)  # Deep brown-black
    draw.ellipse([0, 0, size-1, size-1], fill=vinyl_color)
    
    # Add some groove rings
    groove_color = (40, 25, 15, 255)
    for radius in range(center-10, 70, -8):
        draw.ellipse([center-radius, center-radius, center+radius, center+radius], 
                    outline=groove_color, width=1)
    
    # Golden center label
    label_color = (212, 196, 145, 255)  # Golden label color
    label_radius = 60
    draw.ellipse([center-label_radius, center-label_radius, 
                 center+label_radius, center+label_radius], fill=label_color)
    
    # Inner ring (fixed the bug here)
    ring_color = (139, 69, 19, 255)  # Brown ring
    inner_radius = label_radius - 5
    draw.ellipse([center-inner_radius, center-inner_radius,
                 center+inner_radius, center+inner_radius], outline=ring_color, width=2)
    
    # Add "Spool" text
    try:
        # Try to use a nice font
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        try:
            # Try system fonts
            font = ImageFont.load_default()
        except:
            font = None
    
    # Draw "Spool" text if font available
    if font:
        text = "Spool"
        text_color = (90, 74, 58, 255)  # Dark brown text
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = center - text_width // 2
        text_y = center - text_height // 2
        draw.text((text_x, text_y), text, fill=text_color, font=font)
    else:
        # Draw a simple circle as fallback
        simple_color = (90, 74, 58, 255)
        draw.ellipse([center-10, center-10, center+10, center+10], fill=simple_color)
    
    # Save the icon
    img.save('assets/spool-icon.png', 'PNG')
    print("🎵 Created vinyl disc icon for Spool")

if __name__ == "__main__":
    create_vinyl_icon()