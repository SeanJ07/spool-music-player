# Spiral AI DJ — Smart Shuffle Algorithm

> **Status:** Design doc  
> **Part of:** Spool Music Player  
> **Concept:** The smartest shuffle algorithm ever — it doesn't just randomize, it *mixes*

## The Problem with Normal Shuffle

Standard shuffle = random. It leads to:
- Abrupt genre switches (death metal → ambient lofi)
- Key clashes (C major → F# minor without transition)
- Tempo whiplash (60 BPM → 180 BPM)
- Zero narrative arc — just chaos

## What Spiral DJ Does Instead

It treats your library like a DJ set. Every transition is intentional.

### Data We Extract Per Track

| Attribute | Source | How |
|-----------|--------|-----|
| **BPM** | Audio analysis | librosa beat tracker or Spotify API |
| **Key** | Audio analysis | librosa chroma → Krumhansl-Schmuckler key detection |
| **Energy** | Audio analysis | RMS energy curve → 0-10 |
| **Genre** | Metadata or analysis | ID3 tag → if missing, classify with embeddings |
| **Mood** | Energy + valence | Danceability, acousticness, instrumentalness |
| **Year** | Metadata | ID3 tag |
| **Waveform peaks** | Audio analysis | For beat matching display |
| **Length** | Metadata | For set pacing |

### Transition Scoring

For every possible track pair (A → B), compute a compatibility score:

```
score(A→B) = w1 × keyMatch(A,B) + w2 × bpmMatch(A,B) + w3 × energyCurve(A,B) + w4 × genreContinuity(A,B) + w5 × eraCohesion(A,B) + w6 × novelty
```

**Key Match** (weight: 0.25):
- Perfect: same key → 1.0
- Relative major/minor → 0.9
- Perfect 4th/5th → 0.8 (Camelot Wheel adjacent)
- Clashing: diminished 5th → 0.1

**BPM Match** (weight: 0.25):
- ±3 BPM → 1.0 (no pitch shift needed)
- ±6 BPM → 0.7 (slight adjustment)
- ±12 BPM → 0.4 (major shift, but could double/halve)
- >20 BPM apart → 0.1

**Energy Curve** (weight: 0.20):
- Similar energy → 0.8 (smooth)
- Gradual build → bonus (energy rising over set)
- Drops feel good after peaks → 0.6

**Genre Continuity** (weight: 0.15):
- Same genre/artist → 0.9
- Compatible genres (rock → punk) → 0.7
- Unexpected but interesting → 0.5
- Jarring clash → 0.1

**Era Cohesion** (weight: 0.05):
- Same decade → small bonus
- Intentional era-hopping → neutral

**Novelty** (weight: 0.10):
- Haven't heard this pair recently → bonus
- Avoids repeating the same track too soon

### The Algorithm

```
1. Analyze all tracks in library (cache results for speed)
2. Build a complete transition graph (N×N matrix)
3. Set start track (first song)
4. For each step:
   a. Find top-5 candidates by score
   b. Apply anti-repeat penalty (don't replay within 15 tracks)
   c. Weight by energy curve target (rising/falling/maintaining)
   d. Add slight randomness (ε-greedy, ε=0.1)
   e. Pick winner
5. Optional: user provides "seed" — mood, BPM range, genre
```

## DJ Modes

| Mode | Description | Energy Curve |
|------|-------------|-------------|
| **Flow** | Smooth transitions, key-matched, DJ set | ~ (steady, slight arc) |
| **Rise** | Building intensity, peak → cool-down | ↗ (rising then fall) |
| **Chill** | Stay low-energy, ambient transitions | → (flat, low) |
| **Party** | High energy, bangers only, bold switches | ↗↗ (high, peaking) |
| **Discover** | Maximize novelty, explore library | ~ (variable) |
| **Era Hop** | Journey through decades | — (by year) |

## Prototype Implementation

### Phase 1 — Metadata-Only (No Audio Analysis Needed)
Use ID3 tags + Spotify API for BPM/key/genre. Works for any tagged library.
- Read metadata from files or Spotify playlist
- Build transition matrix
- Generate playlist

### Phase 2 — Audio Analysis
Add librosa for real-time BPM + key detection from raw audio.
- Requires: `pip install librosa`
- Cache results to JSON for instant re-use

### Phase 3 — Live Mixing
- Crossfade between tracks
- Beat-synced transitions
- Pitch shifting to match keys

## Tech Stack

```
┌─────────────────────────────────────────┐
│              Spiral DJ Engine            │
├─────────────────────────────────────────┤
│  Track Analysis    │  Transition Graph   │
│  ┌───────────────┐ │  ┌───────────────┐ │
│  │ librosa       │ │  │ Weighted edges │ │
│  │ (BPM, key)    │ │  │ Dijkstra-like  │ │
│  │ spotipy       │ │  │ path finding   │ │
│  │ (metadata)    │ │  │ Max-flow       │ │
│  └───────────────┘ │  └───────────────┘ │
├────────────────────┴───────────────────┤
│              DJ Mode Selector           │
│  Flow | Rise | Chill | Party | Discover │
├─────────────────────────────────────────┤
│              Playlist Generator          │
│  Output: ordered track list + metadata  │
└─────────────────────────────────────────┘
```

## File Structure

```
projects/ipod-music-player/
├── record-player.html      # Vinyl UI ✅
├── coverflow.html           # Cover Flow UI ✅  
├── spool.html               # Main app ✅
├── ai-dj/
│   ├── analyze.py           # Track analysis pipeline
│   ├── shuffle.py           # Smart shuffle algorithm
│   ├── cache/               # Cached analysis results
│   └── presets/             # DJ mode presets
└── AI-DJ.md                 # This doc
```

## Next Steps

1. Build `analyze.py` — accept a folder of music files, extract BPM + key
2. Build `shuffle.py` — accept analyzed tracks, generate ordered playlist
3. Integrate with record-player.html — "Spiral DJ" button that triggers smart shuffle
4. Add mode selector to UI
