# Quick Start - Current Working Version

This is the **current working version** of Spool that Sam can run immediately.

## What's Working ✅

- **Full GUI music player** with two-screen layout (Library + Now Playing)
- **MP3 import** via File menu or + button
- **Metadata extraction** (artist, title, album, embedded album art, lyrics)
- **Playback controls** (play/pause, prev/next, shuffle, repeat, seek)
- **Volume control** with visual feedback and smooth slider
- **Vinyl widget** that spins during playback with album art
- **Beautiful gold/dark chrome theme** matching the design spec

## Quick Setup

**Windows (Recommended):**
```powershell
# Navigate to the project
cd C:\path\to\spool-music-player

# Install dependencies directly with pip
pip install PySide6 mutagen

# Run the app
python -m spool.main
```

**Alternative: Use Windows Python directly (if WSL has issues):**
```powershell
# Navigate to the project
cd C:\path\to\spool-music-player

# Use Windows Python path
"C:\Users\[USERNAME]\AppData\Local\Programs\Python\Python312\python.exe" -m spool.main
```

**macOS/Linux:**
```bash
cd spool-music-player
pip install PySide6 mutagen
python -m spool.main
```

## How to Test

1. **Launch the app** - You'll see the Library screen with gold content area
2. **Import MP3s** - Click `File → Open MP3 Files…` or the `+` button
3. **Browse Library** - See album thumbnails, artist, and time columns  
4. **Play a track** - Double-click any row to switch to Now Playing and start playback
5. **Try controls:** 
   - Click play/pause to control vinyl spinning
   - Drag seek bar to jump in the track
   - Use volume slider with speaker icon that changes
   - Test prev/next, shuffle, repeat buttons
   - Click ⌂ to return to library without stopping

## Current Architecture

**Key Components:**
- `src/spool/models/track.py` - Track dataclass with album art + lyrics
- `src/spool/services/metadata_service.py` - ID3 tag extraction (mutagen)
- `src/spool/services/library_service.py` - File import (in-place)
- `src/spool/services/playback_queue.py` - Queue/navigation logic
- `src/spool/ui/now_playing_screen.py` - Vinyl + lyrics + transport + volume
- `src/spool/ui/library_screen.py` - Table view with thumbnails
- `src/spool/ui/playback_controller.py` - QMediaPlayer wrapper
- `src/spool/ui/vinyl_widget.py` - Spinning vinyl visualization
- `src/spool/ui/styles.py` - Gold/dark theme

## What's Next

**Immediate priorities:**
- Testing on macOS (ensure cross-platform compatibility)
- Persistence (remember library between sessions)
- Minor UI polish (curved text on vinyl, button feedback)

**Planned features:**
- Cover Flow mode (3D album carousel)
- AI DJ smart shuffle
- Keyboard shortcuts
- Playlist support

## Troubleshooting

**If app doesn't launch:**
- Make sure PySide6 and mutagen are installed: `pip install PySide6 mutagen`
- On WSL, use Windows Python directly (see command above)

**If no sound plays:**
- Check system volume
- Ensure MP3 files have embedded audio (not just metadata)
- Try the volume slider - default is 70%

**If UI looks wrong:**
- Window should have ~12px dark border around gold content
- Vinyl should spin when playing, album art in center
- Volume slider between seek bar and transport controls

---

**Welcome Sam!** 🎵 Feel free to explore the code, test features, and suggest improvements. The codebase is well-structured and ready for collaboration.