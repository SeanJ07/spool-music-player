# Changelog

## 2026-05-28 - Version 0 repository reorganization

### Added

- `PROJECT_VISION.md`
- `VERSION_0_AUDIT.md`
- `ARCHIVE_MANIFEST.md`
- `DEVELOPMENT_NOTES.md`
- `samples/README.md`
- top-level structural folders:
  - `src/`
  - `docs/`
  - `assets/`
  - `tests/`
  - `tools/`
  - `prototypes/` (`web/`, `python/`)
  - `archive/` (`docs/`)
  - `legacy/`
  - `samples/`
  - `config/`

### Changed

- `README.md` rewritten for Version 0 scope and handoff clarity.
- `ROADMAP.md` updated to Version 0-first phased planning.

### Moved

- `ipod_scanner.py` -> `prototypes/python/ipod_scanner.py`
- `spool_launcher.py` -> `prototypes/python/spool_launcher.py`
- `spool.html` -> `prototypes/web/spool.html`
- `record-player.html` -> `prototypes/web/record-player.html`
- `coverflow.html` -> `prototypes/web/coverflow.html`
- `AI-DJ.md` -> `archive/docs/AI-DJ.md`
- `PROPOSAL.md` -> `archive/docs/PROPOSAL.md`
- `SPOOL-HARDWARE.md` -> `archive/docs/SPOOL-HARDWARE.md`
- `sprint-2-plan.md` -> `archive/docs/sprint-2-plan.md`

### Removed

- none (non-destructive migration policy applied)

## 2026-05-28 - Version 0.1 documentation and onboarding pass

### Added

- `CONTRIBUTING.md`
- `docs/INDEX.md`
- `docs/ARCHITECTURE_DECISIONS.md`
- folder-level onboarding docs:
  - `src/README.md`
  - `docs/README.md`
  - `assets/README.md`
  - `tests/README.md`
  - `tools/README.md`
  - `config/README.md`
  - `legacy/README.md`

### Changed

- `ROADMAP.md` expanded with explicit Version 1 handoff sections:
  - what to build first
  - what not to start with
- `ARCHIVE_MANIFEST.md` updated with README/ROADMAP Git recoverability notes.

### Notes

- Prior versions of `README.md` and `ROADMAP.md` remain recoverable through Git history (`git log` / `git show`).

## 2026-05-28 - Version 1 Checkpoint 2 metadata/import foundation

### Added

- `src/spool/services/metadata_service.py`
  - reads basic MP3 metadata with mutagen
  - applies fallback values when tags are missing
  - returns clear success/failure results without crashing
- `src/spool/services/library_service.py`
  - accepts local path list
  - imports `.mp3` files in-place (no file copy/move)
  - returns imported tracks, skipped files, and errors
- `tools/dev_scan_mp3.py`
  - terminal-only helper for testing 1+ local MP3 files before UI work

### Changed

- `src/spool/services/__init__.py` exports import/metadata services.
- `.gitignore` now ignores `samples/media/**` local test media.
- `DEVELOPMENT_NOTES.md` now includes Checkpoint 2 setup/test instructions for:
  - macOS/Linux
  - Windows PowerShell
  - expected output and common failure cases
