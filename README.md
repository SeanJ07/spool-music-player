# Spool

> iPod-inspired music player with turntable visualization and Cover Flow

A nostalgic music player that brings the classic iPod experience to your desktop with modern touches - vinyl record animation, Cover Flow album browsing, and voice integration.

## Features

- **Turntable View** - Vinyl record that spins while playing
- **Cover Flow** - Flip through albums like the classic iPod
- **Voice Commands** - "Spiral, play [album]" integration
- **Local Music Library** - No streaming, your files
- **Minimal UI** - Focus on the music, not the interface

## Tech Stack

- **Python + Tkinter** - Lightweight native UI
- **pygame** - Audio playback
- **mutagen** - MP3 metadata reading
- **Web fallback** - HTML/CSS/JS version available

## Screenshots

```
┌─────────────────────────┐
│      ▶ Now Playing      │
│  ┌───────────────────┐  │
│  │   ┌───────────┐   │  │
│  │   │  VINYL    │   │  │
│  │   │   RECORD  │   │  │
│  │   │  ◄◄   ▶►  │   │  │
│  │   └───────────┘   │  │
│  └───────────────────┘  │
│                         │
│  Track: Midnight City   │
│  Artist: M83           │
│  Album: Hurry Up        │
│  [━━━━━━━━━━━━○] 3:42  │
└─────────────────────────┘
```

## Development

```bash
# Scan music library
python3 ipod_scanner.py

# Launch player
python3 spool_launcher.py

# Or web version
open spool.html
```

## Project Structure

```
ipod-music-player/
├── spool.html          # Main web player
├── coverflow.html      # Cover Flow standalone
├── record-player.html  # Turntable standalone
├── ipod_scanner.py     # Library scanner
└── spool_launcher.py   # Desktop launcher
```

## Future

- Spiral desktop app integration
- AI DJ mode (auto-playlist generation)
- Vinyl crackle effects
- Hardware integration (physical iPod controls)