---
project: spool
status: proposal
created: 2026-05-26
updated: 2026-05-26
---

# Spool — Physical Music Player Hardware

## Concept

A dedicated physical music player device. Drop your music onto it, pick it up, and browse your library with Cover Flow — no phone, no streaming subscription, no distractions. Just music.

**Think:** iPod Touch meets modern hardware. Raspberry Pi heart, aluminum body, touchscreen, headphone jack.

## ⚠️ The Apple Music Reality

Apple Music **subscription** tracks are DRM-locked. They will NOT play on non-Apple hardware. You have two paths:

| Path | What You Get | Vibe |
|------|-------------|------|
| **A — Your Purchased Library** | iTunes Store purchases (DRM-free AAC), ripped CDs, Bandcamp/independent downloads. Drag and drop onto the device like an old iPod. | Legit. Full control. |
| **B — Alternative Sources** | 🏴‍☠️ Not my lane. You handle that. | You know the deal. |

**Recommendation:** Start with Path A. Your purchased iTunes library + anything you've ripped or downloaded. That's probably more music than you remember.

---

## Hardware Build

### Specs

| Component | Choice | Cost | Why |
|-----------|--------|------|-----|
| **Brain** | Raspberry Pi Zero 2 W | ~$15 | Tiny, low power, enough for audio + UI |
| **Screen** | Waveshare 3.5" or 5" TFT touchscreen | ~$25-40 | Fits in hand, iPod-sized |
| **Audio** | HiFiBerry DAC+ Zero or Pimoroni Audio DAC SHIM | ~$20-30 | Clean audio output, not Pi's noisy 3.5mm |
| **Storage** | 128GB microSD | ~$15 | Enough for thousands of songs |
| **Battery** | LiPo 2500mAh + Adafruit PowerBoost 1000C | ~$35 | 6-8 hours playback, USB-C rechargeable |
| **Case** | Custom 3D-printed aluminum-look enclosure | ~$10-20 (filament) | iPod aesthetic, click wheel zone |
| **Controls** | Physical buttons (GPIO) or capacitive touch ring | ~$10 | Tactile feedback |
| **Total Hardware** | | **~$130-165** | |

### Optional Upgrades

| Upgrade | Cost | What |
|---------|------|------|
| Pi 4 + 5" display | +$40 | Faster UI, bigger screen |
| Aluminum CNC case | +$50-100 | Real metal, not printed |
| Bluetooth module | +$10 | Wireless headphones |
| 512GB microSD | +$20 | Massive library |

---

## Phases

### Phase 1 — Hardware Assembly (1-2 weekends)
**Status:** 🔴 Not started
**Cost:** $130-165

- [ ] Order parts (bill of materials below)
- [ ] Assemble Pi + screen + DAC
- [ ] Solder GPIO buttons (play/pause, skip, volume)
- [ ] Flash OS (Raspberry Pi OS Lite) + configure
- [ ] Test audio output through DAC
- [ ] Test touchscreen input
- [ ] 3D-print prototype case

### Phase 2 — Music Software Stack (1 weekend)
**Status:** 🔴 Not started

- [ ] Install Mopidy (music server backend) or build custom player
- [ ] Configure local file library — scans `/music` folder
- [ ] Set up auto-mount for USB transfer (plug into PC → appears as drive → drop music → unplug → plays)
- [ ] SSH access for remote management
- [ ] WiFi for initial setup, optional offline mode
- [ ] Boot directly into music player (kiosk mode)

### Phase 3 — Cover Flow UI (1-2 weekends)
**Status:** 🔴 Not started

- [ ] Custom touchscreen UI — Cover Flow album browsing
- [ ] 3D CSS/WebGL album carousel with reflections
- [ ] Touch gestures — swipe to flip, tap to play, pinch to zoom
- [ ] Now Playing screen with waveform visualizer
- [ ] Dark glass aesthetic (cyan on charcoal)
- [ ] Album art from embedded ID3 tags or folder.jpg
- [ ] Click wheel inspired navigation zone

### Phase 4 — Final Assembly & Polish (1 weekend)
**Status:** 🔴 Not started

- [ ] Final case design — aluminum-style 3D print or CNC
- [ ] Internal cable management
- [ ] Headphone jack + USB-C port cutouts
- [ ] Battery life testing + optimization
- [ ] Screen protector / glass face
- [ ] Lanyard loop (iPod touch nostalgia)
- [ ] Boot screen — "Spool" logo animation

---

## Feature Roadmap

| Priority | Feature | Phase | Dependency |
|----------|---------|-------|------------|
| P0 | Audio playback through DAC | 1 | Parts arrive |
| P0 | Touchscreen display working | 1 | Parts arrive |
| P0 | USB mass storage (drop music from PC) | 2 | OS configured |
| P0 | Local music library scanning | 2 | Storage mounted |
| P1 | Cover Flow album browser | 3 | UI framework chosen |
| P1 | Touch gestures (swipe, tap) | 3 | Touchscreen driver |
| P1 | Now Playing screen | 3 | Audio engine working |
| P2 | Waveform visualizer | 3 | Cover Flow done |
| P2 | Physical buttons (GPIO) | 1 | Soldering |
| P2 | Battery + charging circuit | 1 | PowerBoost |
| P3 | Custom case (3D printed) | 4 | All internals final |
| P3 | Boot animation | 4 | UI done |
| P4 | Bluetooth audio | — | Optional module |
| P5 | WiFi sync (wireless transfer) | — | Post-launch |

---

## Bill of Materials

```
Raspberry Pi Zero 2 W              $15      (PiShop.us / Amazon)
Waveshare 3.5" TFT Touchscreen     $25      (Amazon)
Pimoroni Audio DAC SHIM            $20      (Pimoroni / Amazon)
128GB Samsung microSD              $15      (Amazon)
Adafruit PowerBoost 1000C          $20      (Adafruit)
2500mAh LiPo battery               $15      (Adafruit)
Tactile buttons × 5                $5       (Amazon)
JST connectors + wires             $5       (Amazon)
3D printer filament (PLA)          $10      (already have?)
USB-C breakout board               $5       (Amazon)
3.5mm jack breakout                $3       (Amazon)
                                  ----
TOTAL                             ~$138
```

---

## Timeline Estimate

| Phase | Effort | When |
|-------|--------|------|
| 1 — Hardware Assembly | 2 weekends | After parts arrive (~1 week shipping) |
| 2 — Music Stack | 1 weekend | After Phase 1 |
| 3 — Cover Flow UI | 1-2 weekends | After Phase 2 |
| 4 — Final Polish | 1 weekend | After Phase 3 |
| **Total** | **5-6 weekends** | **~1.5-2 months (hobby pace)** |

---

## Connection to Cyberdeck

This could be a standalone device OR integrated into the cyberdeck build you mentioned wanting. If integrated:

- Share the Raspberry Pi (bigger model)
- Cover Flow as one of the cyberdeck "modes"
- Same battery/power system
- Same case/enclosure

Call it: **Spool module** for the cyberdeck.

---

## Files This Device Plays

- **MP3** — universal
- **AAC / M4A** (DRM-free) — your iTunes purchases
- **FLAC** — lossless for the audiophile in you
- **WAV / AIFF** — raw audio
- **OGG Vorbis** — open source flex
- **ALAC** — Apple lossless

**Does NOT play:** Apple Music subscription tracks (FairPlay DRM), Audible audiobooks (without conversion).

---

## Next Action

**Decision point:** Standalone device or cyberdeck module?

**If yes:** Order parts list. I'll generate a clickable Amazon/Adafruit cart.

**If cyberdeck module:** We spec a bigger Pi and design the enclosure to house both.
