# Spool (Version 0)

Spool is a long-term cross-platform desktop music app project inspired by the iPod experience.

Version 0 is intentionally focused on repository organization, preservation, documentation, and handoff clarity. It is not for implementing production playback features yet.

## Version 0 Scope

Version 0 exists to:

- organize this repository into a scalable structure
- preserve past experiments and partial work safely
- clarify project direction and architecture boundaries
- make collaboration easier for future human and AI contributors

Version 0 does not include feature implementation for playback systems, integrations, or storage backends.

## Current Repository Structure

```text
spool-music-player/
├── src/                  # Future production application source
├── docs/                 # Project documentation space
├── assets/               # Static assets and design material
├── tests/                # Future test suites
├── tools/                # Utility scripts and automation tools
├── prototypes/           # Experimental implementations preserved as reference
│   ├── python/
│   └── web/
├── archive/              # Historical docs and artifacts no longer canonical
│   └── docs/
├── legacy/               # Reserved for old code/systems requiring migration later
├── samples/              # Sample data guidance (no active media committed)
├── config/               # Configuration templates and env conventions
└── *.md                  # Canonical project-level guidance and audit docs
```

## Canonical Docs

- `PROJECT_VISION.md` - product intent and boundaries
- `ROADMAP.md` - phased plan with Version 0 priorities
- `VERSION_0_AUDIT.md` - repository audit findings and review queue
- `ARCHIVE_MANIFEST.md` - preserved historical file map and rationale
- `DEVELOPMENT_NOTES.md` - contributor norms and collaboration notes
- `CHANGELOG.md` - documented repository history

## Where Prior Work Lives

- Web and Python experiments are under `prototypes/`.
- Historical planning and concept documents are under `archive/docs/`.
- Nothing was aggressively rewritten; previous work is preserved for later review.

## Sample Media Policy (Version 0)

Sample MP3 files are for Version 1 testing, not Version 0 implementation.

- Keep local test media out of git.
- Place local files in `samples/media/` when Version 1 testing starts.
- See `samples/README.md` for detailed guidance.