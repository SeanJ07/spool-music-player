"""Minimal playback wrapper around QMediaPlayer + QAudioOutput.

Checkpoint 4 purpose:
- give the UI a small, focused API: play(track), toggle_pause(), stop()
- own the QMediaPlayer/QAudioOutput lifetime so they survive Qt's GC
- expose the underlying player so the window can connect to its signals
"""

from __future__ import annotations

from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer

from spool.models import Track


class PlaybackController:
    """Single-source playback. One track at a time, no queue yet."""

    def __init__(self) -> None:
        self._player = QMediaPlayer()
        self._audio_output = QAudioOutput()
        self._player.setAudioOutput(self._audio_output)
        
        # Start with volume at 70%
        self._audio_output.setVolume(0.7)

    @property
    def player(self) -> QMediaPlayer:
        return self._player

    def play(self, track: Track) -> None:
        self._player.setSource(QUrl.fromLocalFile(str(track.path)))
        self._player.play()

    def toggle_pause(self) -> None:
        if self._player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self._player.pause()
        else:
            self._player.play()

    def stop(self) -> None:
        self._player.stop()

    def set_volume(self, volume: float) -> None:
        """Set volume from 0.0 to 1.0"""
        self._audio_output.setVolume(max(0.0, min(1.0, volume)))

    def get_volume(self) -> float:
        """Get current volume (0.0 to 1.0)"""
        return self._audio_output.volume()
