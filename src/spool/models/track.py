"""Track model for imported local audio files.

Why this file exists:
- keeps all track-related values in one place
- gives the UI and services a shared, predictable data shape
- makes fallback handling explicit when metadata tags are missing
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Track:
    """Represents one local MP3 file in the Version 1 library view.

    Notes for beginners:
    - We store both the real file path and display-friendly text fields.
    - Metadata values may be missing in real MP3 files, so defaults matter.
    - `duration_seconds` stays numeric so formatting can be done in the UI.
    """

    path: Path
    filename: str
    title: str
    artist: str = "Unknown Artist"
    album: str = "Unknown Album"
    duration_seconds: float = 0.0

    def duration_label(self) -> str:
        """Return a mm:ss string for simple display tables.

        This helper is intentionally small so UI code stays easy to read.
        """
        total_seconds = max(0, int(self.duration_seconds))
        minutes, seconds = divmod(total_seconds, 60)
        return f"{minutes}:{seconds:02d}"

