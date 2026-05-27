# Spool Roadmap

> "First you build it. Then you hold it."

---

## Version Path

| Version | What | Hardware | Time | Status |
|---------|------|----------|------|--------|
| **v1.0** | Browser player — audio engine + Cover Flow + visualizer | Your PC | 12 hours | 🔴 Not started |
| **v1.5** | Polish — playlists, queue, library management | Your PC | 4 hours | ⚪ Later |
| **v2.0** | Port to Raspberry Pi — touchscreen kiosk | Pi Zero 2 W + screen | Parts + 2 weekends | ⚪ Later |
| **v2.5** | Custom 3D-printed case + battery | Same Pi | 1 weekend | ⚪ Later |
| **v3.0** | Dedicated device — fully self-contained | Final enclosure | TBD | ⚪ Vision |

---

## v1.0 — Browser Player (NOW)

**Goal:** A working music player in a single HTML file. Drop your music in, browse with Cover Flow, watch the visualizer react. Opens by double-click. Works offline.

**Total time:** ~12 hours (5 sprints)

```
Sprint 1 ─── Sprint 2 ─── Sprint 3 ─── Sprint 4 ─── Sprint 5
[Player]      [Cover Flow]  [Visualizer] [Glass UI]   [Library]
  2-3h          2-3h          2-3h         1-2h         2-3h
```

### Sprint 1 — Core Player
- Audio engine (Web Audio API)
- Play/pause, skip, volume
- Progress bar + seek
- Dark UI shell
- Drag & drop or file picker to load music

### Sprint 2 — Cover Flow
- 3D CSS carousel
- Album art with glass reflections
- Swipe/click to flip albums
- Select to play

### Sprint 3 — Visualizer
- FFT frequency bars
- Waveform display
- Multiple modes (bars → waveform → particles)
- Color extraction from album art

### Sprint 4 — Glass UI
- backdrop-filter blur effects
- Click wheel inspired navigation zone
- Smooth transitions
- Album metadata display

### Sprint 5 — Library
- Playlists, queue, shuffle
- Folder scanning
- Recently played

---

## v1.5 — Polish (LATER)

- Mobile responsive layout
- Keyboard shortcuts
- Mini player mode
- Last.fm scrobbling
- Export playlist as file

---

## v2.0 — Hardware Port (FUTURE)

**Prerequisites:** v1.0 is finished and you love it.

- Order parts (~$138)
- Raspberry Pi OS Lite + touchscreen driver
- Mopidy or custom backend
- v1.0 UI adapted for touchscreen
- Boots directly into player (kiosk mode)
- USB mass storage — plug into PC, drop music, unplug

---

## v3.0 — Final Device (VISION)

- CNC aluminum or polished 3D print enclosure
- Dedicated DAC for audiophile output
- Bluetooth for wireless headphones
- Haptic feedback on scroll
- 8+ hour battery life
- Fits in your pocket

---

## Next Action

**Build Sprint 1 right now** — audio engine + dark UI shell.

Say "build it" and I'll start coding.
