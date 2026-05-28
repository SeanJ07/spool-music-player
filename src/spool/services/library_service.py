"""Library import helpers for local MP3 paths.

Checkpoint 2 purpose:
- accept a list of local paths
- keep files in place (no copying/moving)
- build Track objects in memory
- report skipped files and parse errors clearly
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from spool.models import Track
from spool.services.metadata_service import read_mp3_metadata


@dataclass
class ImportResult:
    """Summary of one import attempt."""

    imported_tracks: list[Track] = field(default_factory=list)
    skipped_files: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def import_mp3_paths(file_paths: list[str | Path]) -> ImportResult:
    """Convert MP3 paths into in-memory Track objects.

    Important behavior:
    - We *reference* the source files only.
    - We do not copy, rename, or modify user music files.
    - We skip non-MP3 paths for Version 1 clarity.
    """

    result = ImportResult()

    for raw_path in file_paths:
        path = Path(raw_path).expanduser()

        # Keep filtering explicit: Version 1 supports .mp3 only.
        if path.suffix.lower() != ".mp3":
            result.skipped_files.append(f"{path} (skipped: only .mp3 supported)")
            continue

        metadata_result = read_mp3_metadata(path)
        if metadata_result.ok and metadata_result.track is not None:
            result.imported_tracks.append(metadata_result.track)
        elif metadata_result.error:
            result.errors.append(f"{path}: {metadata_result.error}")
        else:
            result.errors.append(f"{path}: Unknown metadata import failure.")

    return result

