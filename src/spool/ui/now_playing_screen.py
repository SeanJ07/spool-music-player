"""Now Playing screen — vinyl + lyrics + seek bar + transport controls."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from spool.models import Track
from spool.ui.vinyl_widget import VinylWidget


def _format_time(ms: int) -> str:
    seconds = max(0, ms // 1000)
    return f"{seconds // 60}:{seconds % 60:02d}"


class NowPlayingScreen(QWidget):
    home_clicked = Signal()
    play_pause_clicked = Signal()
    prev_clicked = Signal()
    next_clicked = Signal()
    shuffle_toggled = Signal()
    rewind_clicked = Signal()
    repeat_toggled = Signal()
    seek_requested = Signal(int)
    volume_changed = Signal(float)  # 0.0 to 1.0

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("contentPanel")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self._user_dragging = False
        self._last_shown_seconds = -1

        # --- Header (home button top-right) ---
        self._home_button = QPushButton("⌂")
        self._home_button.setObjectName("circularSmall")
        self._home_button.setToolTip("Library")
        self._home_button.clicked.connect(self.home_clicked)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(20, 20, 20, 8)
        header_layout.addStretch(1)
        header_layout.addWidget(self._home_button)

        # --- Body: vinyl left, lyrics right ---
        self._vinyl = VinylWidget()

        self._lyrics = QTextEdit()
        self._lyrics.setObjectName("lyrics")
        self._lyrics.setReadOnly(True)
        self._lyrics.setFrameShape(QTextEdit.Shape.NoFrame)
        self._lyrics.setPlainText("No lyrics available")

        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(24, 8, 24, 8)
        body_layout.setSpacing(20)
        body_layout.addWidget(self._vinyl, 1)
        body_layout.addWidget(self._lyrics, 1)

        # --- Seek row: position | slider | duration ---
        self._position_label = QLabel("0:00")
        self._position_label.setObjectName("timeLabel")
        self._duration_label = QLabel("0:00")
        self._duration_label.setObjectName("timeLabel")

        self._seek = QSlider(Qt.Orientation.Horizontal)
        self._seek.setObjectName("seekBar")
        self._seek.setMinimum(0)
        self._seek.setMaximum(0)
        self._seek.sliderPressed.connect(self._on_slider_pressed)
        self._seek.sliderReleased.connect(self._on_slider_released)

        seek_layout = QHBoxLayout()
        seek_layout.setContentsMargins(28, 4, 28, 4)
        seek_layout.setSpacing(10)
        seek_layout.addWidget(self._position_label)
        seek_layout.addWidget(self._seek, 1)
        seek_layout.addWidget(self._duration_label)

        # --- Volume row ---
        self._volume_label = QLabel("🔊")
        self._volume_label.setObjectName("volumeLabel")
        
        self._volume = QSlider(Qt.Orientation.Horizontal)
        self._volume.setObjectName("volumeSlider")
        self._volume.setMinimum(0)
        self._volume.setMaximum(100)  # 0-100 for user-friendly display
        self._volume.setValue(70)     # Start at 70%
        self._volume.valueChanged.connect(self._on_volume_changed)

        volume_layout = QHBoxLayout()
        volume_layout.setContentsMargins(28, 2, 28, 8)
        volume_layout.setSpacing(8)
        volume_layout.addWidget(self._volume_label)
        volume_layout.addWidget(self._volume, 1)
        volume_layout.addStretch(1)  # Add some space on the right

        # --- Transport row ---
        self._prev_btn = self._make_small("⏮", self.prev_clicked, "Previous")
        self._next_btn = self._make_small("⏭", self.next_clicked, "Next")
        self._shuffle_btn = self._make_small("🔀", self.shuffle_toggled, "Shuffle")
        self._rewind_btn = self._make_small("⏪", self.rewind_clicked, "Restart track")
        self._play_pause_btn = QPushButton("▶")
        self._play_pause_btn.setObjectName("circularLarge")
        self._play_pause_btn.setToolTip("Play / Pause")
        self._play_pause_btn.clicked.connect(self.play_pause_clicked)
        self._repeat_btn = self._make_small("🔁", self.repeat_toggled, "Repeat")

        transport_layout = QHBoxLayout()
        transport_layout.setContentsMargins(28, 4, 28, 20)
        transport_layout.setSpacing(14)
        transport_layout.addStretch(1)
        transport_layout.addWidget(self._prev_btn)
        transport_layout.addWidget(self._next_btn)
        transport_layout.addWidget(self._shuffle_btn)
        transport_layout.addWidget(self._rewind_btn)
        transport_layout.addWidget(self._play_pause_btn)
        transport_layout.addWidget(self._repeat_btn)
        transport_layout.addStretch(1)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        outer.addLayout(header_layout)
        outer.addLayout(body_layout, 1)
        outer.addLayout(seek_layout)
        outer.addLayout(volume_layout)
        outer.addLayout(transport_layout)

    def _make_small(self, glyph: str, emit_signal, tooltip: str) -> QPushButton:
        btn = QPushButton(glyph)
        btn.setObjectName("circularSmall")
        btn.setToolTip(tooltip)
        btn.clicked.connect(emit_signal)
        return btn

    # --- External API used by MainWindow ---

    def set_track(self, track: Track) -> None:
        self._vinyl.set_track(track)
        self._lyrics.setPlainText(track.lyrics if track.lyrics else "No lyrics available")

    def set_playback_state(self, state: QMediaPlayer.PlaybackState) -> None:
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self._play_pause_btn.setText("⏸")
            self._vinyl.set_spinning(True)
        else:
            self._play_pause_btn.setText("▶")
            self._vinyl.set_spinning(False)

    def set_position(self, position_ms: int) -> None:
        if not self._user_dragging:
            self._seek.setValue(position_ms)
        new_seconds = max(0, position_ms // 1000)
        if new_seconds != self._last_shown_seconds:
            self._last_shown_seconds = new_seconds
            self._position_label.setText(_format_time(position_ms))

    def set_duration(self, duration_ms: int) -> None:
        self._seek.setMaximum(max(0, duration_ms))
        self._duration_label.setText(_format_time(duration_ms))

    def set_shuffle_active(self, active: bool) -> None:
        self._set_button_active(self._shuffle_btn, active)

    def set_repeat_active(self, active: bool) -> None:
        self._set_button_active(self._repeat_btn, active)

    def set_volume(self, volume: float) -> None:
        """Set volume from 0.0 to 1.0 (called from MainWindow)"""
        volume_percent = int(volume * 100)  # Convert to percentage
        self._volume.blockSignals(True)  # Don't emit signal when setting programmatically
        self._volume.setValue(volume_percent)
        self._volume.blockSignals(False)
        
        # Update icon based on volume level
        if volume == 0:
            self._volume_label.setText("🔇")
        elif volume < 0.3:
            self._volume_label.setText("🔈")
        elif volume < 0.7:
            self._volume_label.setText("🔉")
        else:
            self._volume_label.setText("🔊")

    # --- Internal ---

    def _on_volume_changed(self, value: int) -> None:
        """Handle volume slider changes"""
        volume_decimal = value / 100.0  # Convert from percentage to decimal
        self.volume_changed.emit(volume_decimal)
        
        # Update icon based on volume level
        if value == 0:
            self._volume_label.setText("🔇")
        elif value < 30:
            self._volume_label.setText("🔈")
        elif value < 70:
            self._volume_label.setText("🔉")
        else:
            self._volume_label.setText("🔊")

    def _on_slider_pressed(self) -> None:
        self._user_dragging = True

    def _on_slider_released(self) -> None:
        self._user_dragging = False
        self.seek_requested.emit(self._seek.value())

    @staticmethod
    def _set_button_active(button: QPushButton, active: bool) -> None:
        button.setProperty("active", "true" if active else "false")
        style = button.style()
        style.unpolish(button)
        style.polish(button)
