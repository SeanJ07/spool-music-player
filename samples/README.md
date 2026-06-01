# Samples Directory Guidance

This directory is reserved for sample inputs and fixtures.

## Version 0 Policy

- do not implement media ingestion features here
- do not commit personal music files
- keep this folder documentation-only during Version 0

## Version 1 Preparation

When Version 1 testing begins, place local sample media in:

- `samples/media/` (local-only test files)

Recommended local convention:

- `samples/media/mp3/` for MP3 test tracks
- `samples/media/reference/` for optional metadata test notes

## Git Hygiene

- keep media files ignored by git
- use placeholder text files if folder scaffolding needs to be visible without committing actual audio
