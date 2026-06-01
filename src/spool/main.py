"""Application entrypoint for the Spool desktop prototype.

Checkpoint 3: launches the PySide6 main window. The window starts empty;
use File → Open MP3 Files… to import local files via the existing
library_service.
"""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from spool.ui import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
