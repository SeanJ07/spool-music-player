"""Metadata reading helpers for local MP3 files.

Checkpoint 2 purpose:
- read basic metadata from one MP3 path
- return a Track on success
- return a clear error message on failure

This module is intentionally UI-free so we can test it from the terminal first.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from spool.models import Track


@dataclass
class MetadataReadResult:
    """Result container for metadata parsing.

    `track` is populated on success.
    `error` is populated on failure.
    """

    source_path: Path
    track: Track | None = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        """True when metadata parsing produced a valid Track."""
        return self.track is not None and self.error is None


def read_mp3_metadata(file_path: str | Path) -> MetadataReadResult:
    """Read one local MP3 file and convert it into a Track.

    Why this function is defensive:
    - local files can be missing, renamed, or unreadable
    - MP3 tags are often incomplete
    - mutagen may fail on malformed files
    - we never want import flow to crash the app
    """

    path = Path(file_path).expanduser()

    if not path.exists():
        return MetadataReadResult(source_path=path, error="Path does not exist.")

    if not path.is_file():
        return MetadataReadResult(source_path=path, error="Path is not a file.")

    # Version 1 only accepts MP3 files.
    if path.suffix.lower() != ".mp3":
        return MetadataReadResult(source_path=path, error="Only .mp3 files are supported in Version 1.")

    try:
        # Import mutagen here so we can return a clear error message
        # if the dependency is not installed in the active environment yet.
        from mutagen import MutagenError
        from mutagen.mp3 import MP3
    except ImportError as exc:
        return MetadataReadResult(
            source_path=path,
            error=f"mutagen is not installed in this environment: {exc}",
        )

    try:
        # mutagen reads MP3 headers and ID3 tags.
        # Tags may be missing, so we always apply fallback values below.
        audio = MP3(path)
    except (MutagenError, OSError, ValueError) as exc:
        return MetadataReadResult(source_path=path, error=f"Could not parse MP3 metadata: {exc}")

    tags = audio.tags

    # Fallbacks keep the library usable when metadata is incomplete.
    # Many real-world MP3 files are missing artist/album/title tags.
    title = _read_text_tag(tags, "TIT2", fallback=path.stem)
    artist = _read_text_tag(tags, "TPE1", fallback="Unknown Artist")
    album = _read_text_tag(tags, "TALB", fallback="Unknown Album")

    try:
        duration_seconds = float(getattr(audio.info, "length", 0.0) or 0.0)
    except (TypeError, ValueError):
        # Safe fallback for corrupt header duration.
        duration_seconds = 0.0

    track = Track(
        path=path.resolve(),
        filename=path.name,
        title=title,
        artist=artist,
        album=album,
        duration_seconds=duration_seconds,
    )
    return MetadataReadResult(source_path=path, track=track)


def _read_text_tag(tags: object, key: str, fallback: str) -> str:
    """Extract a single text tag value from mutagen tags.

    mutagen can return different tag shapes depending on file content.
    This helper normalizes those shapes into a clean string.
    """

    if not tags:
        return fallback

    value = tags.get(key)
    if not value:
        return fallback

    text_values = getattr(value, "text", None)
    if text_values and len(text_values) > 0:
        text = str(text_values[0]).strip()
        return text if text else fallback

    text = str(value).strip()
    return text if text else fallback

