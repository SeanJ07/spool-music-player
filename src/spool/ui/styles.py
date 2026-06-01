"""Centralized Qt stylesheet for the Spool UI.

Applied at the QMainWindow level so all child widgets inherit.
Colors come from the redesign spec: near-black chrome, warm gold content,
dark circular buttons with white glyphs.
"""

APP_STYLESHEET = """
QMainWindow {
    background-color: #1a1a1a;
}

QWidget#darkFrame {
    background-color: #1a1a1a;
}

QWidget#contentPanel {
    background-color: #D4B483;
}

QLabel#title {
    color: #1a1a1a;
    font-size: 28px;
    font-weight: bold;
}

QLabel#subtitle {
    color: #5a4a30;
    font-size: 12px;
}

QLabel#timeLabel {
    color: #1a1a1a;
    font-size: 11px;
}

QPushButton#circularSmall {
    background-color: #1a1a1a;
    color: white;
    border: 2px solid transparent;
    border-radius: 20px;
    min-width: 36px;
    min-height: 36px;
    max-width: 36px;
    max-height: 36px;
    font-size: 14px;
}

QPushButton#circularSmall:hover {
    background-color: #2c2c2c;
}

QPushButton#circularSmall[active="true"] {
    border: 2px solid #f0d090;
}

QPushButton#circularLarge {
    background-color: #1a1a1a;
    color: white;
    border: 2px solid transparent;
    border-radius: 28px;
    min-width: 52px;
    min-height: 52px;
    max-width: 52px;
    max-height: 52px;
    font-size: 20px;
}

QPushButton#circularLarge:hover {
    background-color: #2c2c2c;
}

QTableView {
    background-color: #D4B483;
    color: #1a1a1a;
    border: none;
    gridline-color: rgba(26, 26, 26, 40);
    selection-background-color: #b89968;
    selection-color: #1a1a1a;
}

QHeaderView::section {
    background-color: #c8a878;
    color: #1a1a1a;
    border: none;
    padding: 6px;
    font-weight: bold;
}

QTextEdit#lyrics {
    background-color: #D4B483;
    color: #1a1a1a;
    border: none;
    font-size: 13px;
}

QTextEdit#lyrics QWidget {
    background-color: #D4B483;
}

QSlider#seekBar::groove:horizontal {
    height: 4px;
    background: #8a7050;
    border-radius: 2px;
}

QSlider#seekBar::handle:horizontal {
    background: #1a1a1a;
    width: 12px;
    margin: -5px 0;
    border-radius: 6px;
}

QSlider#seekBar::sub-page:horizontal {
    background: #1a1a1a;
    border-radius: 2px;
}

/* Volume slider styling */
QLabel#volumeLabel {
    color: #1a1a1a;
    font-size: 16px;
}

QSlider#volumeSlider::groove:horizontal {
    height: 6px;
    background: #8a7050;
    border-radius: 3px;
    margin: 0 8px;
}

QSlider#volumeSlider::handle:horizontal {
    background: #1a1a1a;
    width: 16px;
    height: 16px;
    margin: -8px 0;
    border-radius: 8px;
    border: 2px solid #f0d090;
}

QSlider#volumeSlider::sub-page:horizontal {
    background: #1a1a1a;
    border-radius: 3px;
}

QSlider#volumeSlider:hover::handle:horizontal {
    border-color: #f0e0b0;
}
"""
