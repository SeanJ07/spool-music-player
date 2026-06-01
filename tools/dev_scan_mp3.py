#!/usr/bin/env python3
"""Developer helper to test Checkpoint 2 metadata import from terminal.

This script is intentionally simple:
- accepts one or more file paths
- runs Version 1 import/metadata foundation
- prints readable output for debugging
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow running from repository root without requiring editable install first.
# This keeps beginner testing friction low.
REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from spool.services import import_mp3_paths


def main() -> int:
    """Parse paths, run import service, and print results."""

    parser = argparse.ArgumentParser(
        description="Scan local MP3 files and print parsed metadata."
    )
    parser.add_argument("paths", nargs="+", help="One or more local file paths.")
    args = parser.parse_args()

    print("[Spool][Scan] Starting metadata scan...")
    result = import_mp3_paths(args.paths)

    if result.imported_tracks:
        print(f"[Spool][Scan] Imported {len(result.imported_tracks)} track(s):")
        for index, track in enumerate(result.imported_tracks, start=1):
            print(f"  {index}. {track.filename}")
            print(f"     title    : {track.title}")
            print(f"     artist   : {track.artist}")
            print(f"     album    : {track.album}")
            print(f"     duration : {track.duration_label()} ({track.duration_seconds:.2f}s)")
            print(f"     path     : {track.path}")

    if result.skipped_files:
        print(f"[Spool][Scan] Skipped {len(result.skipped_files)} path(s):")
        for item in result.skipped_files:
            print(f"  - {item}")

    if result.errors:
        print(f"[Spool][Scan] Errors ({len(result.errors)}):")
        for item in result.errors:
            print(f"  - {item}")

    if not result.imported_tracks and not result.skipped_files and not result.errors:
        print("[Spool][Scan] No input paths were processed.")

    print("[Spool][Scan] Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

