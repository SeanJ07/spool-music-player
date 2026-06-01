# Contributing

## Quick Start for New Contributors

**🎵 We have a WORKING desktop music player!** 
See `CONTRIBUTOR_GUIDE.md` for a complete setup guide or `QUICK_START.md` to run immediately.

**What's Ready:**
- Two-screen UI (Library + Now Playing)
- Full MP3 playback with volume control
- Beautiful gold/dark chrome theme
- Spinning vinyl visualization
- Album art and lyrics extraction

**How to Run:**
```bash
pip install PySide6 mutagen
python -m spool.main
```

---

## Project Status

We've moved from "Version 0 documentation phase" to "Version 1 active development" with a working prototype. The core architecture is stable and ready for collaboration.

## Current Focus Areas

**High Priority:**
- Cross-platform testing (especially macOS)
- User feedback and polish
- Persistence (save/load library state)

**Medium Priority:**
- Keyboard shortcuts
- Playlist support
- Cover Flow mode

**Future:**
- AI DJ smart shuffle
- Web versions
- Hardware integration

## How to Contribute

### Code Contributions
1. Fork the repository
2. Create a feature branch
3. Test thoroughly on your platform
4. Submit a PR with clear description of changes

### Testing & Feedback
- Run the app and report any issues
- Test with different MP3 files (various tags, art, etc.)
- Try edge cases (very long tracks, special characters, etc.)
- Share UX suggestions

### Areas Needing Expertise
- **macOS developers** - Test and fix platform-specific issues
- **UI/UX designers** - Refine the visual design
- **Audio engineers** - Improve playback quality and features

## Architecture Overview

**Key Components:**
- `src/spool/models/track.py` - Track dataclass
- `src/spool/services/` - Business logic (metadata, import, playback queue)
- `src/spool/ui/` - PySide6 GUI components
- `src/spool/ui/playback_controller.py` - QMediaPlayer wrapper

**Design Principles:**
- Local-first (no streaming services)
- Cross-platform (Windows + macOS primary)
- Clean separation of concerns
- Signal/slot pattern for UI communication

## Development Guidelines

**Code Style:**
- Type hints everywhere
- Clear docstrings
- Follow existing patterns
- Test UI changes manually

**File Organization:**
- New features in appropriate `src/` subdirectories
- Experiments go to `prototypes/` first
- Maintain the folder structure from `DEVELOPMENT_NOTES.md`

**Testing:**
- Test with various MP3 files
- Verify UI responsiveness
- Check performance with large libraries

## Collaboration Rules

- Preserve existing functionality
- Document breaking changes
- Keep commits focused and descriptive
- Ask questions before major changes

---
