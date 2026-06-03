"""Now Playing screen — spool mechanism with tape-unwinding timeline per UI specifications."""

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
    QListWidget,
    QListWidgetItem,
)
from PySide6.QtGui import QPainter, QPainterPath, QPen, QColor, QFont

from spool.models import Track
from spool.ui.vinyl_widget import VinylWidget


def _format_time(ms: int) -> str:
    seconds = max(0, ms // 1000)
    return f"{seconds // 60}:{seconds % 60:02d}"


class TapeSpoolTimeline(QWidget):
    """Timeline that emerges from the vinyl spool like unwinding tape."""
    
    def __init__(self):
        super().__init__()
        self.setFixedHeight(80)
        self.setObjectName("tapeSpoolTimeline")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        
        # Draw tape unwinding effect from left (spool) to right
        tape_color = QColor(218, 196, 177)  # Golden tape color
        
        # Create path for tape ribbon
        path = QPainterPath()
        
        # Start near left edge (where spool is)
        start_x = 150
        end_x = rect.width() - 40
        
        # Tape ribbon with slight wave to simulate unwinding
        path.moveTo(start_x, rect.height() // 2)
        path.cubicTo(
            start_x + 50, rect.height() // 2 - 10,
            start_x + 100, rect.height() // 2 + 10,
            end_x, rect.height() // 2
        )
        
        # Draw main tape ribbon
        pen = QPen(tape_color, 12, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.drawPath(path)
        
        # Draw centerline (tape track)
        center_pen = QPen(QColor(139, 69, 19), 2, Qt.PenStyle.DashLine)
        painter.setPen(center_pen)
        painter.drawPath(path)
        
        # Draw tape tears/texture marks
        texture_pen = QPen(QColor(218, 196, 177, 150), 1)
        painter.setPen(texture_pen)
        for i in range(start_x + 20, end_x, 15):
            painter.drawLine(i, rect.height() // 2 - 6, i + 5, rect.height() // 2 + 6)


class NowPlayingScreen(QWidget):
    home_clicked = Signal()
    play_pause_clicked = Signal()
    prev_clicked = Signal()
    next_clicked = Signal()
    shuffle_clicked = Signal()
    shuffle_toggled = Signal(bool)
    repeat_clicked = Signal()
    repeat_toggled = Signal(bool)
    seek_back_clicked = Signal()
    seek_requested = Signal(int)
    volume_changed = Signal(float)
    view_toggled = Signal(str)  # "lyrics" or "queue"

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("contentPanel")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        # Header with home button (top-right)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 24, 24, 0)
        header_layout.addStretch()  # Push home button to the right
        
        self._home_button = QPushButton("⌂")
        self._home_button.setObjectName("homeButton")
        self._home_button.setToolTip("Back to Library")
        self._home_button.clicked.connect(self.home_clicked)
        
        header_layout.addWidget(self._home_button)
        
        # Main content: vinyl on left, lyrics on right
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(24, 24, 24, 12)
        content_layout.setSpacing(40)
        
        # Vinyl widget (spool mechanism) on the left
        self._vinyl_widget = VinylWidget()
        self._vinyl_widget.setFixedSize(280, 280)
        
        # Dynamic content area (Lyrics/Queue toggle)
        self._content_widget = QWidget()
        self._content_layout = QVBoxLayout(self._content_widget)
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        self._content_layout.setSpacing(8)
        
        # Toggle button for Lyrics/Queue view
        self._toggle_button = QPushButton("📝 Lyrics")
        self._toggle_button.setObjectName("circularButton")
        self._toggle_button.clicked.connect(self._on_view_toggled)
        self._toggle_button.setFixedSize(80, 36)
        
        # Queue panel for upcoming tracks
        self._queue_panel = QListWidget()
        self._queue_panel.setObjectName("queuePanel")
        self._queue_panel.setFixedSize(320, 230)
        
        # Style queue panel to match the aesthetic
        self._queue_panel.setStyleSheet("""
            QListWidget#queuePanel {
                background-color: #e6d5a8;
                border: 2px solid #d4c491;
                color: #5a4a3a;
                font-family: 'SF Pro Text', 'Helvetica Neue', Arial, sans-serif;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #d4c491;
            }
            QListWidget::item:selected {
                background-color: #d4c491;
            }
        """)
        
        # Lyrics panel
        self._lyrics_panel = QTextEdit()
        self._lyrics_panel.setObjectName("lyricsPanel")
        self._lyrics_panel.setReadOnly(True)
        self._lyrics_panel.setPlainText("No lyrics available")
        self._lyrics_panel.setFixedSize(320, 230)
        
        # Initially show lyrics, hide queue
        self._queue_panel.hide()
        
        # Add widgets to content layout
        self._content_layout.addWidget(self._toggle_button)
        self._content_layout.addWidget(self._lyrics_panel)
        self._content_layout.addWidget(self._queue_panel)
        
        content_layout.addWidget(self._vinyl_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self._content_widget)

        # Tape-spool timeline
        self._tape_timeline = TapeSpoolTimeline()
        
        # Time labels below timeline
        time_layout = QHBoxLayout()
        time_layout.setContentsMargins(24, 8, 24, 0)
        
        self._current_time_label = QLabel("0:00")
        self._current_time_label.setObjectName("timeLabel")
        
        self._duration_label = QLabel("0:00")
        self._duration_label.setObjectName("timeLabel")
        self._duration_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        time_layout.addWidget(self._current_time_label)
        time_layout.addStretch()
        time_layout.addWidget(self._duration_label)
        
        # Seek bar (positioned below tape timeline)
        self._seek_slider = QSlider(Qt.Orientation.Horizontal)
        self._seek_slider.setObjectName("seekBar")
        self._seek_slider.setRange(0, 0)
        self._seek_slider.setValue(0)

        # Transport controls (rectangular footer)
        transport = QWidget()
        transport.setObjectName("transportWidget")
        transport.setFixedHeight(56)
        
        transport_layout = QHBoxLayout(transport)
        transport_layout.setContentsMargins(12, 8, 12, 8)
        transport_layout.setSpacing(8)
        
        # Transport buttons in order: Prev | Next | Shuffle | Rewind | Play/Pause | Repeat
        self._prev_button = QPushButton("⏮")
        self._prev_button.setObjectName("transportButton")
        self._prev_button.clicked.connect(self.prev_clicked)
        
        self._next_button = QPushButton("⏭")
        self._next_button.setObjectName("transportButton")
        self._next_button.clicked.connect(self.next_clicked)
        
        self._shuffle_button = QPushButton("🔀")
        self._shuffle_button.setObjectName("transportButton")
        self._shuffle_button.setCheckable(True)
        self._shuffle_button.clicked.connect(self.shuffle_clicked)
        
        self._rewind_button = QPushButton("⏪")
        self._rewind_button.setObjectName("transportButton")
        self._rewind_button.clicked.connect(self.seek_back_clicked)
        
        self._play_pause_button = QPushButton("▶")
        self._play_pause_button.setObjectName("transportButton")
        self._play_pause_button.clicked.connect(self.play_pause_clicked)
        
        self._repeat_button = QPushButton("🔁")
        self._repeat_button.setObjectName("transportButton")
        self._repeat_button.setCheckable(True)
        self._repeat_button.clicked.connect(self.repeat_clicked)
        
        transport_layout.addWidget(self._prev_button)
        transport_layout.addWidget(self._next_button)
        transport_layout.addWidget(self._shuffle_button)
        transport_layout.addWidget(self._rewind_button)
        transport_layout.addWidget(self._play_pause_button)
        transport_layout.addWidget(self._repeat_button)
        
        # Volume slider
        transport_layout.addStretch()
        self._volume_slider = QSlider(Qt.Orientation.Horizontal)
        self._volume_slider.setObjectName("volumeSlider")
        self._volume_slider.setRange(0, 100)
        self._volume_slider.setValue(70)
        self._volume_slider.setFixedSize(80, 20)
        self._volume_slider.valueChanged.connect(self._on_volume_changed)
        transport_layout.addWidget(self._volume_slider)

        # Main layout assembly
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 24)
        main_layout.setSpacing(0)
        main_layout.addLayout(header_layout)
        main_layout.addLayout(content_layout)
        main_layout.addSpacing(24)
        main_layout.addWidget(self._tape_timeline)
        main_layout.addLayout(time_layout)
        main_layout.addWidget(self._seek_slider)
        main_layout.addSpacing(16)  # Space before transport
        main_layout.addWidget(transport, alignment=Qt.AlignmentFlag.AlignCenter)

        # Connections
        self._seek_slider.sliderReleased.connect(self._on_released)
        
        # Shuffle button toggle handling
        self._shuffle_button.toggled.connect(self._on_shuffle_toggled)
        self._repeat_button.toggled.connect(self._on_repeat_toggled)

    def set_track(self, track: Track | None) -> None:
        """Update UI for the current track."""
        if track:
            self._vinyl_widget.set_track(track)
            # Set lyrics if available
            if track.lyrics:
                self._lyrics_panel.setPlainText(track.lyrics)
            else:
                self._lyrics_panel.setPlainText("No lyrics available")
        else:
            self._vinyl_widget.clear_track()
            self._lyrics_panel.setPlainText("No track loaded")

    def set_duration(self, duration_ms: int) -> None:
        """Set the track duration."""
        self._seek_slider.setRange(0, duration_ms)
        self._duration_label.setText(_format_time(duration_ms))

    def set_position(self, position_ms: int) -> None:
        """Update the playback position (only when user isn't dragging)."""
        if not self._seek_slider.isSliderDown():
            self._seek_slider.setValue(position_ms)
        self._current_time_label.setText(_format_time(position_ms))

    def set_shuffle(self, enabled: bool) -> None:
        """Set shuffle state."""
        self._shuffle_button.setChecked(enabled)

    def set_repeat(self, enabled: bool) -> None:
        """Set repeat state."""
        self._repeat_button.setChecked(enabled)

    def set_is_playing(self, is_playing: bool) -> None:
        """Update play/pause button state."""
        if is_playing:
            self._play_pause_button.setText("⏸")
            self._vinyl_widget.start_rotation()
        else:
            self._play_pause_button.setText("▶")
            self._vinyl_widget.stop_rotation()

    def seek(self, position_ms: int) -> None:
        """Seek to the position (connected to sliderMoved signal)."""
        # Emit seek requested for main window to handle
        self.seek_requested.emit(position_ms)

    def _on_released(self) -> None:
        """Handle seek slider release - perform actual seek."""
        position_ms = self._seek_slider.value()
        self.seek_requested.emit(position_ms)
    
    def _on_shuffle_toggled(self, checked: bool) -> None:
        """Handle shuffle toggle state change."""
        self.shuffle_toggled.emit(checked)
    
    def _on_repeat_toggled(self, checked: bool) -> None:
        """Handle repeat toggle state change."""
        self.repeat_toggled.emit(checked)

    def set_volume(self, volume: float) -> None:
        """Set volume from external source (like main window)."""
        # Convert 0.0-1.0 range to 0-100 slider range
        volume_percent = int(volume * 100)
        self._volume_slider.setValue(volume_percent)
    
    def _on_view_toggled(self) -> None:
        """Toggle between lyrics and queue view."""
        if self._lyrics_panel.isVisible():
            # Show queue, hide lyrics
            self._lyrics_panel.hide()
            self._queue_panel.show()
            self._toggle_button.setText("📋 Queue")
            self.view_toggled.emit("queue")
        else:
            # Show lyrics, hide queue
            self._queue_panel.hide()
            self._lyrics_panel.show()
            self._toggle_button.setText("📝 Lyrics")
            self.view_toggled.emit("lyrics")
    
    def _on_volume_changed(self, volume_percent: int) -> None:
        """Handle volume slider change."""
        volume_float = volume_percent / 100.0
        self.volume_changed.emit(volume_float)
    
    def update_queue(self, tracks: list) -> None:
        """Update the queue panel with upcoming tracks."""
        self._queue_panel.clear()
        for track in tracks:
            item = QListWidgetItem(f"{track.title} - {track.artist}")
            self._queue_panel.addItem(item)