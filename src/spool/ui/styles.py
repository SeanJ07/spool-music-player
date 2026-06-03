"""Centralized Qt stylesheet for the Spool UI.

Applied at the QMainWindow level so all child widgets inherit.
Updated to 2000s golden-yellow aesthetic per UI specifications.
"""

APP_STYLESHEET = """
QMainWindow {
    background-color: #2a2118;
}

QWidget#darkFrame {
    background-color: #2a2118;
}

QWidget#contentPanel {
    background-color: #e6d5a8;
}

/* Header styling */
QLabel#headerLabel {
    color: #5a4a3a;
    font-size: 28px;
    font-weight: bold;
    font-family: 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
}

/* Library view table */
QTableView {
    background-color: #e6d5a8;
    border: none;
    gridline-color: #d4c491;
    selection-background-color: #d4c491;
}

QTableView::item {
    padding: 12px;
    border: none;
    color: #5a4a3a;
}

QTableView::item:selected {
    background-color: #d4c491;
}

/* Album column delegate - thumbnail above name */
QLabel#albumThumbnail {
    background-color: #f0e6d3;
    border: 2px solid #d4c491;
}

/* Circular buttons for header controls */
QPushButton#circularButton {
    background-color: #5a4a3a;
    border: 2px solid #7a6a5a;
    border-radius: 18px;
    min-width: 36px;
    min-height: 36px;
    max-width: 36px;
    max-height: 36px;
    color: #e6d5a8;
    font-size: 18px;
}

QPushButton#circularButton:hover {
    background-color: #7a6a5a;
    border-color: #8a7a6a;
}

QPushButton#circularButton:pressed {
    background-color: #4a3a2a;
}

/* Home button for expanded view */
QPushButton#homeButton {
    background-color: #5a4a3a;
    border: 2px solid #7a6a5a;
    border-radius: 20px;
    min-width: 40px;
    min-height: 40px;
    max-width: 40px;
    max-height: 40px;
    color: #e6d5a8;
    font-size: 20px;
}

QPushButton#homeButton:hover {
    background-color: #7a6a5a;
}

/* vinyl widget styling */
QWidget#vinylWidget {
    background-color: #2a2118;
}

QLabel#vinylDisc {
    background-color: #1a0f08;
    border-radius: 150px;
}

QLabel#vinylLabel {
    background-color: #d4c491;
    border-radius: 60px;
}

QLabel#vinylText {
    color: #5a4a3a;
    font-family: 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
}

/* Lyrics panel */
QTextEdit#lyricsPanel {
    background-color: #e6d5a8;
    border: 2px solid #d4c491;
    color: #5a4a3a;
    font-family: 'SF Pro Text', 'Helvetica Neue', Arial, sans-serif;
    font-size: 16px;
    padding: 16px;
}

QTextEdit#lyricsPanel QScrollBar:vertical {
    background-color: #d4c491;
    width: 12px;
    border-radius: 6px;
}

QTextEdit#lyricsPanel QScrollBar::handle:vertical {
    background-color: #7a6a5a;
    min-height: 20px;
    border-radius: 6px;
}

/* Seek bar */
QSlider#seekBar {
    background-color: transparent;
}

QSlider#seekBar::groove:horizontal {
    background-color: #d4c491;
    height: 8px;
    border-radius: 4px;
}

QSlider#seekBar::handle:horizontal {
    background-color: #5a4a3a;
    border: 2px solid #7a6a5a;
    width: 20px;
    height: 20px;
    border-radius: 10px;
    margin: -6px 0;
}

/* Time labels */
QLabel#timeLabel {
    color: #5a4a3a;
    font-family: 'SF Pro Text', 'Helvetica Neue', Arial, sans-serif;
    font-size: 14px;
}

/* Transport controls - rectangular footer */
QWidget#transportWidget {
    background-color: #5a4a3a;
    border-radius: 8px;
}

QPushButton#transportButton {
    background-color: #2a2118;
    border: none;
    border-radius: 4px;
    min-width: 50px;
    min-height: 40px;
    max-width: 70px;
    color: #e6d5a8;
    font-size: 18px;
    font-family: 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
}

QPushButton#transportButton:hover {
    background-color: #3a2a18;
}

QPushButton#transportButton:pressed {
    background-color: #1a0a08;
}

QPushButton#transportButton[toggled="true"] {
    border: 2px solid #e6d5a8;
}

/* Volume slider */
QSlider#volumeSlider {
    background-color: transparent;
}

QSlider#volumeSlider::groove:horizontal {
    background-color: #d4c491;
    height: 6px;
    border-radius: 3px;
}

QSlider#volumeSlider::handle:horizontal {
    background-color: #5a4a3a;
    border: 1px solid #7a6a5a;
    width: 16px;
    height: 16px;
    border-radius: 8px;
    margin: -5px 0;
}

/* Import dialog styling */
QFileDialog {
    background-color: #e6d5a8;
}

QFileDialog QHeaderView::section {
    background-color: #5a4a3a;
    color: #e6d5a8;
}

QFileDialog QListView::item:selected {
    background-color: #d4c491;
    color: #5a4a3a;
}
"""