---
project: spool
status: proposal
created: 2026-05-26
---

# Spool — iPod Touch-Inspired Music Player

## Concept

A browser-based music player that captures the soul of the iPod Touch — Cover Flow, click wheel aesthetic, dark glass UI, and buttery animations — running entirely in the browser with local file playback.

## Why

Spotify owns playback. Apple Music owns the ecosystem. But nobody owns the *experience* anymore — the tactile joy of flipping through albums, the visual weight of Cover Flow, the satisfaction of a polished, single-purpose device. Spool brings that back as a web app Sean can actually use and show off.

## Visual Identity

| Element | Value |
|---------|-------|
| **Primary surface** | Dark glass — `#1a1a2e` with 80% opacity frosted glass |
| **Accent** | Electric cyan — `#00d4ff` (play button, progress, highlights) |
| **Secondary** | Warm white — `#f0e6d3` (text, artist names) |
| **Background** | Animated gradient — deep navy to twilight purple (`#0f0f23` → `#1a1033`) |
| **Cover Flow** | 3D CSS perspective carousel, album art tilting at ±45° |
| **Font** | SF Pro Display (system) or Inter as fallback |

## Phases

### Phase 1 — Core Player (Sprint 1)
**Status:** Not started
**Timeline:** 2-3 hours

- [ ] Audio engine — Web Audio API with local file loading (drag & drop + file picker)
- [ ] Play/pause, skip forward/back, volume slider
- [ ] Progress bar with seek
- [ ] Minimal dark UI — album art + controls
- [ ] Now Playing display — artwork, title, artist, album
- [ ] Single HTML file, self-contained

### Phase 2 — Cover Flow (Sprint 2)
**Status:** Not started
**Timeline:** 2-3 hours

- [ ] CSS 3D Cover Flow carousel
- [ ] Album art reflection + glass effect
- [ ] Click/swipe to flip through albums
- [ ] Center-select plays that album
- [ ] Smooth spring animations (60fps)
- [ ] Track listing slides up from bottom

### Phase 3 — Visualizer (Sprint 3)
**Status:** Not started  
**Timeline:** 2-3 hours

- [ ] Canvas-based audio visualizer (FFT frequency bars)
- [ ] Waveform display behind Cover Flow
- [ ] Reacts to currently playing track
- [ ] Multiple visualizer modes toggle (bars → waveform → particle ring)
- [ ] Color matches album art dominant color

### Phase 4 — Polish & Details (Sprint 4)
**Status:** Not started
**Timeline:** 1-2 hours

- [ ] Glass morphism effects — backdrop-filter blur
- [ ] Click wheel inspired gesture zone (bottom area)
- [ ] "Now Playing" transition animations
- [ ] Battery/time status bar (iPod nostalgia)
- [ ] Album metadata from ID3 tags
- [ ] Keyboard shortcuts (Space=play, arrows=skip)
- [ ] Responsive — works on desktop, decent on mobile

### Phase 5 — Library & Playlists (Sprint 5)
**Status:** Not started
**Timeline:** 2-3 hours

- [ ] Music library — scan folder, build index
- [ ] Playlists — create, edit, reorder
- [ ] Shuffle + repeat modes
- [ ] Queue system
- [ ] Search/filter library
- [ ] Recently played history

---

## Feature Roadmap

| Priority | Feature | Phase | Effort |
|----------|---------|-------|--------|
| P0 | Audio playback (local files) | 1 | ⭐⭐ |
| P0 | Play/pause/skip/volume | 1 | ⭐ |
| P0 | Dark glass UI shell | 1 | ⭐⭐ |
| P1 | Cover Flow carousel | 2 | ⭐⭐⭐ |
| P1 | Album art + reflection | 2 | ⭐⭐ |
| P2 | Audio visualizer | 3 | ⭐⭐⭐ |
| P2 | Visualizer modes | 3 | ⭐⭐ |
| P2 | Glass morphism polish | 4 | ⭐⭐ |
| P3 | Click wheel zone | 4 | ⭐ |
| P3 | Playlists | 5 | ⭐⭐ |
| P3 | Queue system | 5 | ⭐⭐ |
| P4 | Folder scanning | 5 | ⭐ |
| P4 | ID3 metadata | 4 | ⭐ |
| P5 | Mobile responsive | 4 | ⭐⭐ |

---

## Tech Stack

| Layer | Choice | Why |
|-------|--------|-----|
| **Audio** | Web Audio API | Native, fast, FFT for visualizer |
| **UI** | HTML/CSS/JS (vanilla) | Single file, no build step |
| **Cover Flow** | CSS 3D transforms + perspective | GPU-accelerated, smooth |
| **Visualizer** | Canvas 2D + AnalyserNode | Real-time FFT, low latency |
| **Metadata** | music-metadata-browser (CDN) | ID3 tags from local files |
| **Font** | Inter (Google Fonts) | Sleek, variable weight |

## Deliverables

- `spool.html` — single self-contained file
- Demo track (royalty-free) preloaded for instant wow factor
- Opens by double-click, works offline

## Total Estimated Build Time

**10-14 hours** across 5 sprints

---

## Next Action

Start sprint 1 — build the audio engine and shell UI. Sean gives the green light.
