# Spool

A cross-platform desktop music player built around the feeling of using an iPod — turntable visualization, Cover Flow browsing, the works. Started because I wanted something that actually looked good on a desktop and felt intentional, not just another media player.

This is Version 0. That means the repo is organized, documented, and ready for real development — not a dumping ground of half-finished ideas. Prior experiments are preserved under `prototypes/`, old docs under `archive/`, and the structure is set up so future work has somewhere clean to land.

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

🎵 **WORKING VERSION AVAILABLE!** 

Spool now has a fully functional desktop music player with GUI. See `QUICK_START.md` to run it immediately.

**Current Features:**
- Two-screen UI (Library + Now Playing)  
- MP3 import via menu or + button
- Full metadata extraction (art, lyrics, tags)
- Playback controls with volume slider
- Spinning vinyl visualization
- Beautiful gold/dark chrome theme

**Next Phase:** Persistence, macOS testing, Cover Flow mode.

---

---

*Long-term project. Built because I wanted it to exist.*
