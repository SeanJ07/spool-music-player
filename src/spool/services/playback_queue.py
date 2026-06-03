"""Ordered playback queue with shuffle and repeat state.

Pure Python — no Qt dependency. MainWindow combines this with the
Qt-side PlaybackController to drive playback.
"""

from __future__ import annotations

import random

from spool.models import Track


class PlaybackQueue:
    """Holds the current track list and which one is selected."""

    def __init__(self) -> None:
        self._tracks: list[Track] = []
        self._current_index: int = -1
        self._shuffle: bool = False
        self._repeat: bool = False

    @property
    def shuffle(self) -> bool:
        return self._shuffle

    @property
    def repeat(self) -> bool:
        return self._repeat

    @property
    def current_index(self) -> int:
        return self._current_index

    def set_tracks(self, tracks: list[Track]) -> None:
        self._tracks = list(tracks)
        self._current_index = -1

    def current(self) -> Track | None:
        if 0 <= self._current_index < len(self._tracks):
            return self._tracks[self._current_index]
        return None

    def select(self, index: int) -> Track | None:
        if 0 <= index < len(self._tracks):
            self._current_index = index
            return self._tracks[index]
        return None

    def next(self) -> Track | None:
        if not self._tracks:
            return None
        if self._shuffle and len(self._tracks) > 1:
            candidates = [i for i in range(len(self._tracks)) if i != self._current_index]
            self._current_index = random.choice(candidates)
        else:
            self._current_index = (self._current_index + 1) % len(self._tracks)
        return self._tracks[self._current_index]

    def prev(self) -> Track | None:
        if not self._tracks:
            return None
        if self._current_index <= 0:
            self._current_index = len(self._tracks) - 1
        else:
            self._current_index -= 1
        return self._tracks[self._current_index]

    def toggle_shuffle(self) -> bool:
        self._shuffle = not self._shuffle
        return self._shuffle

    def toggle_repeat(self) -> bool:
        self._repeat = not self._repeat
        return self._repeat

    def get_upcoming_tracks(self) -> list[Track]:
        """Get tracks in order for display (showing upcoming tracks first)."""
        if self._current_index < 0 or self._current_index >= len(self._tracks):
            return self._tracks.copy()
        
        # Return current and upcoming tracks first, then wrap around
        upcoming = self._tracks[self._current_index:] + self._tracks[:self._current_index]
        return upcoming
