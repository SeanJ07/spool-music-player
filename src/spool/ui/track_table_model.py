"""Qt table model exposing tracks to the Library screen.

Three display columns matching the redesign spec: Album, Artist, Time.
The Album column also provides a thumbnail QPixmap via DecorationRole,
which AlbumColumnDelegate uses to paint the thumbnail above the album name.
"""

from __future__ import annotations

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QPixmap

from spool.models import Track


THUMB_SIZE = 56


class TrackTableModel(QAbstractTableModel):
    COLUMN_ALBUM = 0
    COLUMN_ARTIST = 1
    COLUMN_TIME = 2

    HEADERS = ("Album", "Artist", "Time")

    def __init__(self, tracks: list[Track] | None = None) -> None:
        super().__init__()
        self._tracks: list[Track] = list(tracks) if tracks else []
        self._thumbnails: dict[int, QPixmap] = {}

    def set_tracks(self, tracks: list[Track]) -> None:
        self.beginResetModel()
        self._tracks = list(tracks)
        self._thumbnails.clear()
        self.endResetModel()

    def track_at(self, row: int) -> Track | None:
        if 0 <= row < len(self._tracks):
            return self._tracks[row]
        return None

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self._tracks)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self.HEADERS)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        track = self._tracks[index.row()]
        column = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            if column == self.COLUMN_ALBUM:
                return track.album
            if column == self.COLUMN_ARTIST:
                return track.artist
            if column == self.COLUMN_TIME:
                return track.duration_label()
            return None

        if role == Qt.ItemDataRole.DecorationRole and column == self.COLUMN_ALBUM:
            return self._thumbnail_for_row(index.row(), track)

        if role == Qt.ItemDataRole.TextAlignmentRole and column == self.COLUMN_TIME:
            return int(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)

        return None

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal and 0 <= section < len(self.HEADERS):
            return self.HEADERS[section]
        if orientation == Qt.Orientation.Vertical:
            return section + 1
        return None

    def _thumbnail_for_row(self, row: int, track: Track) -> QPixmap | None:
        cached = self._thumbnails.get(row)
        if cached is not None:
            return cached
        if not track.album_art_data:
            return None
        pixmap = QPixmap()
        loaded = pixmap.loadFromData(track.album_art_data)
        if not loaded or pixmap.isNull():
            return None
        scaled = pixmap.scaled(
            THUMB_SIZE,
            THUMB_SIZE,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )
        self._thumbnails[row] = scaled
        return scaled
