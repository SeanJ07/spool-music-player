# Spool

Desktop music player built around the feel of an iPod — turntable visualization, Cover Flow browsing, the works. Made because modern music apps forgot what real objects feel like.

Version 0. Repo is organized and ready for real development. Prior experiments under `prototypes/`, old docs under `archive/`.

**Stack:** Python + HTML (prototypes), targeting cross-platform desktop for v1

---

### What's Here
spool-music-player/
├── src/              # Production source (v1+)
├── docs/             # Project documentation
├── assets/           # Design assets and static files
├── tests/            # Test suites (v1+)
├── tools/            # Utility scripts
├── prototypes/       # Past experiments — Python and web versions
├── archive/          # Old docs, preserved for reference
├── legacy/           # Old systems flagged for future migration
├── samples/          # Sample data guidance (no media committed)
└── config/           # Config templates and env conventions

### Key Docs

- `PROJECT_VISION.md` — what this is and isn't
- `ROADMAP.md` — phased plan, v0 through v1+
- `DEVELOPMENT_NOTES.md` — contributor norms
- `CHANGELOG.md` — history of repo changes
- `VERSION_0_AUDIT.md` — audit of everything in the repo and what to do with it

### Status

Working version available. See `QUICK_START.md` to run it.

**Current features:**
- Two-screen UI (Library + Now Playing)
- MP3 import via menu or + button
- Full metadata extraction (art, lyrics, tags)
- Playback controls with volume slider
- Spinning vinyl visualization
- Gold/dark chrome theme

**Next:** Persistence, macOS testing, Cover Flow mode.

---

*Long-term project. Built because I wanted it to exist.*