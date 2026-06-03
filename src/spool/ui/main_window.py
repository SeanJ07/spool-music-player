"""Main application window — orchestrates the two screens via QStackedWidget.

Wires:
- LibraryScreen signals → import flow, screen switch, queue selection
- NowPlayingScreen signals → playback controller + queue navigation
- PlaybackController player signals → NowPlayingScreen visual state
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from spool.services import PlaybackQueue, import_mp3_paths
from spool.ui.library_screen import LibraryScreen
from spool.ui.now_playing_screen import NowPlayingScreen
from spool.ui.playback_controller import PlaybackController
from spool.ui.styles import APP_STYLESHEET
from spool.ui.track_table_model import TrackTableModel


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Spool")
        self.resize(1100, 720)
        self.setStyleSheet(APP_STYLESHEET)

        self._model = TrackTableModel()
        self._controller = PlaybackController()
        self._queue = PlaybackQueue()

        self._library_screen = LibraryScreen(self._model)
        self._now_playing_screen = NowPlayingScreen()

        self._stack = QStackedWidget()
        self._stack.addWidget(self._library_screen)
        self._stack.addWidget(self._now_playing_screen)

        frame = QWidget()
        frame.setObjectName("darkFrame")
        frame.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(12, 12, 12, 12)
        frame_layout.addWidget(self._stack)
        self.setCentralWidget(frame)

        self._build_menu()
        self._wire_signals()
        
        # Initialize volume slider with controller's current volume
        initial_volume = self._controller.get_volume()
        self._now_playing_screen.set_volume(initial_volume)

    def _build_menu(self) -> None:
        open_action = QAction("&Open MP3 Files…", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self._on_open_files)

        quit_action = QAction("&Quit", self)
        quit_action.setShortcut(QKeySequence.StandardKey.Quit)
        quit_action.triggered.connect(self.close)

        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(quit_action)

    def _wire_signals(self) -> None:
        lib = self._library_screen
        lib.import_clicked.connect(self._on_open_files)
        lib.expand_clicked.connect(self._show_now_playing)
        lib.track_activated.connect(self._on_track_activated)

        nps = self._now_playing_screen
        nps.home_clicked.connect(self._show_library)
        nps.play_pause_clicked.connect(self._controller.toggle_pause)
        nps.prev_clicked.connect(self._on_prev)
        nps.next_clicked.connect(self._on_next)
        nps.shuffle_toggled.connect(self._on_shuffle)
        nps.seek_back_clicked.connect(self._on_rewind)
        nps.repeat_toggled.connect(self._on_repeat)
        nps.seek_requested.connect(self._controller.player.setPosition)
        nps.volume_changed.connect(self._on_volume_changed)
        nps.view_toggled.connect(self._on_view_toggled)

        player = self._controller.player
        player.playbackStateChanged.connect(nps.set_is_playing)
        player.positionChanged.connect(nps.set_position)
        player.durationChanged.connect(nps.set_duration)
        player.mediaStatusChanged.connect(self._on_media_status)
        player.errorOccurred.connect(self._on_player_error)

    # --- Actions ---

    def _on_open_files(self) -> None:
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Open MP3 Files", "", "MP3 Files (*.mp3);;All Files (*)"
        )
        if not paths:
            return
        result = import_mp3_paths(paths)
        self._model.set_tracks(result.imported_tracks)
        self._queue.set_tracks(result.imported_tracks)
        self.statusBar().showMessage(
            f"Imported {len(result.imported_tracks)} — "
            f"Skipped {len(result.skipped_files)} — "
            f"Errors {len(result.errors)}"
        )

    def _show_library(self) -> None:
        self._stack.setCurrentWidget(self._library_screen)

    def _show_now_playing(self) -> None:
        self._stack.setCurrentWidget(self._now_playing_screen)

    def _on_track_activated(self, row: int) -> None:
        track = self._queue.select(row)
        if track is None:
            return
        self._now_playing_screen.set_track(track)
        self._show_now_playing()
        self._controller.play(track)

    def _on_prev(self) -> None:
        track = self._queue.prev()
        if track is None:
            return
        self._now_playing_screen.set_track(track)
        self._controller.play(track)

    def _on_next(self) -> None:
        track = self._queue.next()
        if track is None:
            return
        self._now_playing_screen.set_track(track)
        self._controller.play(track)

    def _on_shuffle(self) -> None:
        active = self._queue.toggle_shuffle()
        self._now_playing_screen.set_shuffle_active(active)

    def _on_repeat(self) -> None:
        active = self._queue.toggle_repeat()
        self._now_playing_screen.set_repeat_active(active)

    def _on_rewind(self) -> None:
        self._controller.player.setPosition(0)

    def _on_media_status(self, status: QMediaPlayer.MediaStatus) -> None:
        if status != QMediaPlayer.MediaStatus.EndOfMedia:
            return
        if self._queue.repeat:
            current = self._queue.current()
            if current is not None:
                self._controller.play(current)
            return
        track = self._queue.next()
        if track is None:
            return
        self._now_playing_screen.set_track(track)
        self._controller.play(track)

    def _on_volume_changed(self, volume: float) -> None:
        """Handle volume changes from the UI."""
        self._controller.set_volume(volume)
    
    def _on_view_toggled(self, view_type: str) -> None:
        """Handle toggle between lyrics and queue view."""
        if view_type == "queue":
            # Update the now playing screen with current queue
            queue_tracks = self._queue.get_upcoming_tracks()
            self._now_playing_screen.update_queue(queue_tracks)

    def _on_player_error(
        self, error: QMediaPlayer.Error, error_string: str
    ) -> None:
        if error == QMediaPlayer.Error.NoError:
            return
        self.statusBar().showMessage(f"Playback error: {error_string}")
