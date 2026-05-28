---
project: spool
sprint: 2
status: completed
completed: 2026-05-27
---

# Spool Sprint 2 — Cover Flow ✅ COMPLETED

## What We're Building

The iconic Cover Flow album browser. Albums tilt at ±45° in a 3D carousel, reflections underneath, smooth spring animations. Tap/click to center-select an album and play it.

## Technical Approach

CSS 3D transforms with `perspective` and `rotateY` for the carousel. No library — pure CSS + vanilla JS. GPU-accelerated with `will-change: transform` and `transform-style: preserve-3d`.

## Features

- ✅ 3D perspective carousel
- ✅ ±45° tilt on side albums
- ✅ Center album scales up + brightens
- ✅ Album art reflections (CSS pseudo-element with `scaleY(-1)` + gradient mask)
- ✅ Click left/right arrows to rotate
- ✅ Click center album to play
- ✅ Spring physics for momentum-based scrolling
- ✅ Glass morphism background behind carousel
- ✅ Keyboard navigation (Arrow keys, Space to play)
- ✅ Drag & drop file support
- ✅ Auto-reconnect to previously picked folder

## Files

- `coverflow.html` — Standalone Cover Flow interface

## Next Sprint Ideas

- Merge Cover Flow into main `spool.html` as a view mode
- Add album art extraction from MP3 metadata (ID3 album art)
- Add AI DJ integration button