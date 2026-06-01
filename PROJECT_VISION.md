# Project Vision

## Mission

Spool aims to become a cross-platform desktop music app inspired by the clarity, tactility, and focus of classic iPod-era listening experiences.

## Product Direction

- initial target platforms: Windows and macOS
- initial build direction: Python-based prototype path
- planned GUI framework: PySide6 (Qt for Python)
- possible future low-level/device-oriented modules: C++

## Version 0 Intent

Version 0 is foundation work only. It prepares the repository and team workflow before feature-heavy development starts.

Version 0 priorities:

- preserve earlier experiments and partially completed work
- organize source and documentation into predictable locations
- document decisions, assumptions, and historical context
- reduce future onboarding friction for both humans and AI agents

## Version 1 Focus (Later)

Version 1 is expected to target:

- local MP3 import
- metadata management
- playlists
- offline playback
- library organization

## Non-Goals During Version 0

- implementing production playback systems
- building drag/drop import as a final feature
- implementing XML parsing pipelines
- adding Apple Music integration
- introducing database layers
- broad architecture rewrites without review documentation

## Collaboration Philosophy

- preserve first, then prune with evidence
- keep docs explicit enough to survive personnel/tooling changes
- prefer simple, maintainable structures over clever abstractions
- ensure all significant moves are traceable in audit and changelog docs
