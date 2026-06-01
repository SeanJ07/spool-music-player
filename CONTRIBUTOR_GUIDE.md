# Setup Guide for New Contributors

## Welcome Sam! 👋

This guide will get you running Spool quickly. The project has a **working desktop music player** ready for testing and development.

## Quick Start (5 minutes)

### 1. Clone and Navigate
```bash
git clone https://github.com/seanjenkins/spool-music-player.git
cd spool-music-player
```

### 2. Install Dependencies
**Windows (Recommended):**
```powershell
pip install PySide6 mutagen
```

**macOS/Linux:**
```bash
pip install PySide6 mutagen
```

### 3. Run the App
```bash
python -m spool.main
```

**That's it!** You should see the Spool music player window appear.

## Project Structure

```
src/spool/
├── models/track.py          # Track dataclass with album art + lyrics
├── services/
│   ├── metadata_service.py  # ID3 tag extraction (mutagen)  
│   ├── library_service.py   # File import (in-place)
│   └── playback_queue.py   # Queue/navigation logic
├── ui/
│   ├── now_playing_screen.py # Vinyl + lyrics + transport + volume
│   ├── library_screen.py     # Table view with thumbnails
│   ├── playback_controller.py # QMediaPlayer wrapper
│   ├── vinyl_widget.py       # Spinning vinyl visualization
│   └── styles.py             # Gold/dark theme
└── main.py                   # App entrypoint
```

## How It Works

**Two-Screen Architecture:**
1. **Library Screen** - Browse your music collection with album thumbnails
2. **Now Playing Screen** - Vinyl visualization + playback controls + volume

**Key Features:**
- Import MP3s via File → Open MP3 Files… or the + button
- Double-click tracks to play
- Volume control with dynamic speaker icon  
- Spinning vinyl during playback
- Lyrics display (from USLT tags or fallback)

## Testing Guide

**Basic Workflow:**
1. Launch app → Library screen appears
2. Click `File → Open MP3 Files…` → Select some music
3. See table with album thumbnails
4. Double-click any track → Switches to Now Playing + starts music
5. Try play/pause, volume, seek, prev/next, shuffle, repeat

**Expected Behavior:**
- Window has dark border around gold content area
- Album art shows in vinyl center during playback
- Vinyl spins when playing, stops when paused
- Volume slider between seek bar and transport controls
- Speaker icon changes: 🔇→🔈→🔉→🔊 based on volume

## Development Guidelines

**Tech Stack:**
- Python 3.11+
- PySide6 (Qt for Python)  
- mutagen (MP3 metadata)
- QMediaPlayer (audio playback)

**Architecture Principles:**
- Local-first (no streaming)
- Windows + macOS primary (Linux secondary)
- In-place import (no file copying)
- Clean separation between services and UI

**Code Style:**
- Type hints everywhere
- Clear docstrings
- Signal/slot pattern for UI communication
- Service layer for business logic

## Contributing

**What to work on:**
1. **Testing** - Run on macOS, report any platform differences
2. **UI Polish** - Refine vinyl text curves, button hover states
3. **Persistence** - Save/load library between sessions
4. **Features** - Keyboard shortcuts, playlists, Cover Flow mode

**How to contribute:**
1. Fork the repo
2. Create a feature branch
3. Test thoroughly
4. Submit a PR with clear description

**Questions?** 
- Check `DEVELOPMENT_NOTES.md` for detailed setup
- Look at `QUICK_START.md` for current status
- Test with sample MP3s in `samples/media/mp3/` (don't commit)

---

**Enjoy building Spool!** 🎵 This is a passion project to make desktop music players feel intentional and beautiful again.