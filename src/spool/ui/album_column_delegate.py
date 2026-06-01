"""Custom delegate for the Album column.

Paints a square thumbnail at the top of the cell with the album name
centered below it. Qt's default item rendering puts the decoration to
the left of the text, so a custom delegate is required for image-above-text.
"""

from __future__ import annotations

from PySide6.QtCore import QModelIndex, QRect, QSize, Qt
from PySide6.QtGui import QColor, QPainter, QPixmap
from PySide6.QtWidgets import QStyle, QStyledItemDelegate, QStyleOptionViewItem


THUMB_SIZE = 56
PADDING = 6
TEXT_HEIGHT = 22


class AlbumColumnDelegate(QStyledItemDelegate):
    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> None:
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if option.state & QStyle.StateFlag.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())

        rect = option.rect
        thumb_x = rect.x() + (rect.width() - THUMB_SIZE) // 2
        thumb_y = rect.y() + PADDING

        decoration = index.data(Qt.ItemDataRole.DecorationRole)
        if isinstance(decoration, QPixmap) and not decoration.isNull():
            painter.drawPixmap(thumb_x, thumb_y, THUMB_SIZE, THUMB_SIZE, decoration)
        else:
            painter.fillRect(
                thumb_x, thumb_y, THUMB_SIZE, THUMB_SIZE, QColor("#5a4a30")
            )

        name = index.data(Qt.ItemDataRole.DisplayRole) or ""
        text_rect = QRect(
            rect.x() + 4,
            thumb_y + THUMB_SIZE + 2,
            rect.width() - 8,
            TEXT_HEIGHT,
        )
        painter.setPen(QColor("#1a1a1a"))
        painter.drawText(
            text_rect,
            int(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop),
            str(name),
        )
        painter.restore()

    def sizeHint(
        self, option: QStyleOptionViewItem, index: QModelIndex
    ) -> QSize:
        return QSize(THUMB_SIZE + 2 * PADDING, THUMB_SIZE + TEXT_HEIGHT + 2 * PADDING)
