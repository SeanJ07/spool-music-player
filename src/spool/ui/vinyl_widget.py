"""Rotating vinyl widget for the Now Playing screen.

Draws a dark vinyl disc with concentric groove rings, the album art
clipped into a center label, and the track title / artist as curved
text along the top and bottom arcs of the label. The entire painter
is rotated by `self._angle` so everything spins together — matching
how a real vinyl label rotates with the disc.

Rotation: ~8 seconds per full turn at 30 FPS → 1.5° per frame.
"""

from __future__ import annotations

import math

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import (
    QColor,
    QFont,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
)
from PySide6.QtWidgets import QWidget

from spool.models import Track


FRAME_INTERVAL_MS = 33
DEGREES_PER_FRAME = 360.0 / (8.0 * (1000.0 / FRAME_INTERVAL_MS))


class VinylWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setMinimumSize(280, 280)
        self._angle: float = 0.0
        self._album_pixmap: QPixmap | None = None
        self._title: str = ""
        self._artist: str = ""

        self._timer = QTimer(self)
        self._timer.setInterval(FRAME_INTERVAL_MS)
        self._timer.timeout.connect(self._on_tick)

    def set_track(self, track: Track) -> None:
        self._title = track.title or ""
        self._artist = track.artist or ""
        self._album_pixmap = None
        if track.album_art_data:
            pix = QPixmap()
            if pix.loadFromData(track.album_art_data) and not pix.isNull():
                self._album_pixmap = pix
        self.update()

    def set_spinning(self, spinning: bool) -> None:
        if spinning and not self._timer.isActive():
            self._timer.start()
        elif not spinning and self._timer.isActive():
            self._timer.stop()

    def _on_tick(self) -> None:
        self._angle = (self._angle + DEGREES_PER_FRAME) % 360.0
        self.update()

    def paintEvent(self, event) -> None:  # noqa: ARG002
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        side = min(self.width(), self.height())
        cx = self.width() / 2.0
        cy = self.height() / 2.0
        vinyl_radius = side / 2.0 - 6.0
        label_radius = vinyl_radius * 0.42

        painter.translate(cx, cy)
        painter.rotate(self._angle)

        # Vinyl disc
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#1a1a1a"))
        painter.drawEllipse(QPointF(0, 0), vinyl_radius, vinyl_radius)

        # Subtle concentric grooves
        groove_pen = QPen(QColor(255, 255, 255, 14))
        groove_pen.setWidth(1)
        painter.setPen(groove_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        groove_start = int(label_radius) + 8
        for r in range(groove_start, int(vinyl_radius) - 2, 4):
            painter.drawEllipse(QPointF(0, 0), float(r), float(r))

        # Album label area
        if self._album_pixmap is not None:
            painter.save()
            clip = QPainterPath()
            clip.addEllipse(QPointF(0, 0), label_radius, label_radius)
            painter.setClipPath(clip)
            target = QRectF(
                -label_radius, -label_radius, label_radius * 2, label_radius * 2
            )
            painter.drawPixmap(
                target, self._album_pixmap, QRectF(self._album_pixmap.rect())
            )
            painter.restore()
        else:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor("#3a3a3a"))
            painter.drawEllipse(QPointF(0, 0), label_radius, label_radius)
            painter.setBrush(QColor("#1a1a1a"))
            painter.drawEllipse(QPointF(0, 0), label_radius * 0.18, label_radius * 0.18)

        # Curved text between label and outer edge
        text_radius = (vinyl_radius + label_radius) / 2.0
        text_font = QFont()
        text_font.setPointSize(max(8, int(label_radius * 0.13)))
        text_font.setBold(True)
        painter.setFont(text_font)
        self._draw_curved_text(painter, self._title, text_radius, on_top=True)
        self._draw_curved_text(painter, self._artist, text_radius, on_top=False)

    def _draw_curved_text(
        self,
        painter: QPainter,
        text: str,
        radius: float,
        on_top: bool,
    ) -> None:
        if not text or radius <= 0:
            return
        fm = painter.fontMetrics()
        total_width = fm.horizontalAdvance(text)
        if total_width <= 0:
            return
        # Cap text arc to half the circle so it doesn't wrap into itself
        max_arc_rad = math.pi * 0.85
        total_arc_rad = min(total_width / radius, max_arc_rad)
        total_arc_deg = math.degrees(total_arc_rad)

        if on_top:
            # Top of circle in Qt coords is angle -90°; left to right = increasing angle
            center_angle_deg = -90.0
            start_angle_deg = center_angle_deg - total_arc_deg / 2.0
            direction = 1.0
            tangent_offset_deg = 90.0
        else:
            # Bottom of circle is +90°; left to right (viewer) = decreasing angle
            center_angle_deg = 90.0
            start_angle_deg = center_angle_deg + total_arc_deg / 2.0
            direction = -1.0
            tangent_offset_deg = -90.0

        # Scale per-char arc so the full text fits the capped arc
        per_char_scale = total_arc_rad / (total_width / radius) if total_width > 0 else 1.0
        current_angle_deg = start_angle_deg
        painter.setPen(QColor("white"))

        for ch in text:
            ch_width = fm.horizontalAdvance(ch)
            ch_arc_rad = (ch_width / radius) * per_char_scale
            ch_arc_deg = math.degrees(ch_arc_rad)
            ch_center_deg = current_angle_deg + direction * ch_arc_deg / 2.0

            rad = math.radians(ch_center_deg)
            x = radius * math.cos(rad)
            y = radius * math.sin(rad)

            painter.save()
            painter.translate(x, y)
            painter.rotate(ch_center_deg + tangent_offset_deg)
            painter.drawText(QPointF(-ch_width / 2.0, 0.0), ch)
            painter.restore()

            current_angle_deg += direction * ch_arc_deg
