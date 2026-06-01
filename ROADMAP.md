# Spool Roadmap

This roadmap reflects the Version 0 directive: organize first, build later.

## Phase Overview

| Phase | Focus | Status |
|------|------|------|
| Version 0 | Repository organization, preservation, documentation, handoff clarity | In progress |
| Version 1 | Core desktop app prototype (Python + PySide6) | Not started |
| Version 2+ | Platform expansion, polish, possible device integration | Future |

## Version 0 (Current)

### Goals

- establish a clean, scalable repository structure
- preserve experiments and historical planning without losing context
- define canonical documentation and contributor expectations
- reduce ambiguity between prototype work and future production work

### Deliverables

- finalized top-level directory layout
- archived historical docs under `archive/docs/`
- prototypes organized under `prototypes/web/` and `prototypes/python/`
- canonical planning and audit documents at repository root
- clear sample media policy for future testing

### Out of Scope

- production playback implementation
- drag/drop import systems as a deliverable
- XML parsing systems
- Apple Music integration
- database implementation
- major architecture rewrites without explicit review

## Version 1 (Planned, Not Started)

When Version 0 is complete and reviewed, Version 1 is expected to begin with:

- local MP3 import workflows
- metadata reading and management
- simple local library view
- offline playback
- basic playlist and library organization

Primary prototype stack target: Python + PySide6.

### Version 1 Handoff - Build First

- local MP3 import (local files only)
- metadata reading (ID3/basic tag extraction)
- simple library browsing UI
- local offline playback

### Version 1 Handoff - Do Not Start With

- Apple Music API integration
- XML import pipelines
- hardware sync/device integration
- cloud accounts or account systems
- complex database architecture before core local flow is proven

## Version 2+ (Future)

- deeper platform hardening for Windows/macOS
- performance tuning and UX polish
- potential C++ low-level/device modules if required
- optional hardware/device integration after core app maturity

## Immediate Next Step

Complete Version 0 audit follow-up items listed in `VERSION_0_AUDIT.md`, then confirm readiness gate for Version 1 planning.

Version 1 checkpoint note:

- Checkpoint 2 focuses on metadata/import logic only (no UI shell or playback yet).
