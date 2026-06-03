"""Library screen — home view with 3-column grid layout per UI specifications."""

from __future__ import annotations

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QFont

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

        # Header: "Spool" text on left, expand button on right
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(24, 24, 24, 12)
        
        self._title_label = QLabel("Spool")
        self._title_label.setObjectName("headerLabel")
        
        # Expand button on right
        self._expand_button = QPushButton("⛶")
        self._expand_button.setObjectName("circularButton")
        self._expand_button.setToolTip("Expand to Player View")
        self._expand_button.clicked.connect(self.expand_clicked)
        
        header_layout.addWidget(self._title_label)
        header_layout.addStretch()
        header_layout.addWidget(self._expand_button)

        # Table setup with 3 columns: Album | Artist | Time
        self._table_view = QTableView()
        self._table_view.setModel(model)
        self._table_view.setShowGrid(True)  # Enable vertical dividers
        self._table_view.verticalHeader().setVisible(False)
        self._table_view.setAlternatingRowColors(False)
        
        # Set column widths for the 3-column layout
        header = self._table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        
        # Album column (widest for thumbnails)
        self._table_view.setColumnWidth(0, 280)
        # Artist column (medium)
        self._table_view.setColumnWidth(1, 200) 
        # Time column (narrow)
        self._table_view.setColumnWidth(2, 80)
        
        # Set table height to show about 8 rows without scrolling
        self._table_view.setFixedHeight(400)
        
        # Custom album column delegate for thumbnails
        self._table_view.setItemDelegateForColumn(0, AlbumColumnDelegate(self._table_view))
        
        # Import button positioned in the top-right corner of the table area
        import_layout = QHBoxLayout()
        import_layout.setContentsMargins(0, 0, 0, 0)
        
        self._import_button = QPushButton("+")
        self._import_button.setObjectName("circularButton")
        self._import_button.setToolTip("Import MP3 Files")
        self._import_button.clicked.connect(self.import_clicked)
        self._import_button.setFixedSize(36, 36)
        
        # Set up import button layout in the right side area
        import_layout.addStretch()
        import_layout.addWidget(self._import_button)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addLayout(header_layout)
        
        # Import controls above table
        main_layout.addLayout(import_layout)
        main_layout.addSpacing(8)
        
        # Table with proper spacing
        main_layout.addWidget(self._table_view, alignment=Qt.AlignmentFlag.AlignCenter)

        # Connections
        self._table_view.clicked.connect(self._on_table_clicked)
        self._table_view.doubleClicked.connect(self._on_table_activated)

    def update_track_count(self, count: int) -> None:
        """Update the track count display - can be hidden per spec if not needed"""
        pass  # Not showing track count per simplified UI spec

    def _on_table_clicked(self, index: QModelIndex) -> None:
        """Handle click on table row"""
        if index.isValid():
            track_row = index.row()
            self.track_activated.emit(track_row)

    def _on_table_activated(self, index: QModelIndex) -> None:
        """Handle double-click to start playing and switch views"""
        if index.isValid():
            track_row = index.row()
            self.track_activated.emit(track_row)
            
            # Also trigger expand to player view
            self.expand_clicked.emit()

    def set_model(self, model: TrackTableModel) -> None:
        """Update the table model"""
        self._model = model
        self._table_view.setModel(model)
        
        # Refresh delegate when model changes
        if hasattr(self, '_table_view'):
            self._table_view.setItemDelegateForColumn(0, AlbumColumnDelegate(self._table_view))