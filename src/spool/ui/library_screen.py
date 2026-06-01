"""Library screen — header row plus a 3-column track table."""

from __future__ import annotations

from PySide6.QtCore import QModelIndex, Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from spool.ui.album_column_delegate import AlbumColumnDelegate
from spool.ui.track_table_model import TrackTableModel


class LibraryScreen(QWidget):
    track_activated = Signal(int)
    expand_clicked = Signal()
    import_clicked = Signal()

    def __init__(self, model: TrackTableModel) -> None:
        super().__init__()
        self._model = model
        self.setObjectName("contentPanel")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self._title_label = QLabel("Spool")
        self._title_label.setObjectName("title")

        self._subtitle_label = QLabel("0 tracks")
        self._subtitle_label.setObjectName("subtitle")

        title_box = QVBoxLayout()
        title_box.setContentsMargins(0, 0, 0, 0)
        title_box.setSpacing(2)
        title_box.addWidget(self._title_label)
        title_box.addWidget(self._subtitle_label)

        self._import_button = QPushButton("+")
        self._import_button.setObjectName("circularSmall")
        self._import_button.setToolTip("Import MP3 files")
        self._import_button.clicked.connect(self.import_clicked)

        self._expand_button = QPushButton("⛶")  # ⛶
        self._expand_button.setObjectName("circularSmall")
        self._expand_button.setToolTip("Now Playing")
        self._expand_button.clicked.connect(self.expand_clicked)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(20, 20, 20, 12)
        header_layout.setSpacing(8)
        header_layout.addLayout(title_box)
        header_layout.addStretch(1)
        header_layout.addWidget(self._import_button)
        header_layout.addWidget(self._expand_button)

        self._table = QTableView()
        self._table.setModel(self._model)
        self._table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self._table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self._table.setShowGrid(False)
        self._table.verticalHeader().setVisible(False)
        self._table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self._table.setItemDelegateForColumn(
            TrackTableModel.COLUMN_ALBUM, AlbumColumnDelegate(self._table)
        )
        self._table.verticalHeader().setDefaultSectionSize(98)
        self._table.doubleClicked.connect(self._on_double_clicked)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addLayout(header_layout)
        layout.addWidget(self._table, 1)

        self._model.modelReset.connect(self._refresh_subtitle)
        self._refresh_subtitle()

    def _on_double_clicked(self, index: QModelIndex) -> None:
        if index.isValid():
            self.track_activated.emit(index.row())

    def _refresh_subtitle(self) -> None:
        count = self._model.rowCount()
        word = "track" if count == 1 else "tracks"
        self._subtitle_label.setText(f"{count} {word}")
