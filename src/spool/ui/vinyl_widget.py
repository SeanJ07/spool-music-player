"""Rotating vinyl widget for the Now Playing screen - enhanced for 2000s aesthetic.

Draws a dark vinyl disc with concentric groove rings, the album art
clipped into a center label, and improved curved text along the label perimeter.
Enhanced spinning animation and golden-yellow theming.
"""

from __future__ import annotations

import math

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import (
    QColor,
    QFont,
    QFontMetrics,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QTransform,
)
from PySide6.QtWidgets import QWidget

from spool.models import Track


FRAME_INTERVAL_MS = 33
DEGREES_PER_FRAME = 360.0 / (8.0 * (1000.0 / FRAME_INTERVAL_MS))


class VinylWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setMinimumSize(280, 280)
        self.setObjectName("vinylWidget")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        self._angle: float = 0.0
        self._album_pixmap: QPixmap | None = None
        self._title: str = ""
        self._artist: str = ""

        self._timer = QTimer(self)
        self._timer.setInterval(FRAME_INTERVAL_MS)
        self._timer.timeout.connect(self._on_tick)

    def set_track(self, track: Track) -> None:
        """Load track information and album art."""
        self._title = track.title or ""
        self._artist = track.artist or ""
        self._album_pixmap = None
        
        if track.album_art_data and track.album_art_mime:
            # Load album art from binary data
            pixmap = QPixmap()
            if pixmap.loadFromData(track.album_art_data, track.album_art_mime):
                self._album_pixmap = pixmap

        self.update()

    def clear_track(self) -> None:
        """Clear current track data."""
        self._title = ""
        self._artist = ""
        self._album_pixmap = None
        self.update()

    def start_rotation(self) -> None:
        """Begin spinning animation."""
        if not self._timer.isActive():
            self._timer.start()

    def stop_rotation(self) -> None:
        """Halt spinning animation."""
        self._timer.stop()

    def paintEvent(self, event) -> None:
        """Main painting method - draws the complete vinyl assembly."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Apply rotation to the entire vinyl disc
        center = QPointF(self.width() / 2, self.height() / 2)
        painter.translate(center)
        painter.rotate(-self._angle)  # Negative for clockwise rotation
        painter.translate(-center)

        # Draw vinyl disc
        self._draw_vinyl_disc(painter)

        # Draw center label with album art
        self._draw_center_label(painter)

        # Draw curved text on the label perimeter
        self._draw_curved_text(painter)

    def _draw_vinyl_disc(self, painter: QPainter) -> None:
        """Draw the dark vinyl disc with concentric grooves."""
        rect = self.rect()
        disc_radius = min(rect.width(), rect.height()) // 2 - 20
        
        # Dark vinyl color
        disc_color = QColor(26, 15, 8)  # Deep brown-black
        painter.setBrush(disc_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(rect.center(), disc_radius, disc_radius)
        
        # Draw concentric groove rings
        groove_color = QColor(40, 25, 15)
        groove_pen = QPen(groove_color, 1)
        painter.setPen(groove_pen)
        
        # Inner grooves
        for radius in range(disc_radius - 20, 70, -8):
            painter.drawEllipse(rect.center(), radius, radius)

    def _draw_center_label(self, painter: QPainter) -> None:
        """Draw the center label area with album art or placeholder."""
        center = QPointF(self.width() / 2, self.height() / 2)
        label_radius = 60
        
        # Label background
        label_color = QColor(212, 196, 145)  # Golden label color
        painter.setBrush(label_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center, label_radius, label_radius)
        
        # Inner ring detail
        ring_pen = QPen(QColor(139, 69, 19), 2)  # Brown ring
        painter.setPen(ring_pen)
        painter.drawEllipse(center, label_radius - 5, label_radius - 5)
        
        # Album art or placeholder
        if self._album_pixmap:
            # Scale and crop album art to fit the label circle
            square_size = label_radius * 2 - 20  # Leave margin for ring
            scaled_art = self._album_pixmap.scaled(
                square_size, square_size,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            
            # Create circular clip
            art_rect = QRectF(
                center.x() - square_size // 2,
                center.y() - square_size // 2,
                square_size,
                square_size
            )
            painter.setClipPath(self._create_circle_path(center, label_radius - 10))
            painter.drawPixmap(art_rect, scaled_art, scaled_art.rect())
            painter.setClipRect(self.rect())  # Reset clipping
        else:
            # Placeholder "Original" text or icon
            placeholder_color = QColor(90, 74, 58)
            painter.setPen(placeholder_color)
            font = QFont("SF Pro Display", 14, QFont.Weight.Bold)
            painter.setFont(font)
            painter.drawText(center, "Original")

    def _draw_curved_text(self, painter: QPainter) -> None:
        """Draw title and artist curved along the label perimeter."""
        center = QPointF(self.width() / 2, self.height() / 2)
        text_radius = 75  # Radius where curved text appears
        
        text_color = QColor(90, 74, 58)
        painter.setPen(text_color)
        font = QFont("SF Pro Display", 11, QFont.Weight.Medium)
        painter.setFont(font)
        
        # Title on top arc
        if self._title:
            self._draw_curved_text_line(painter, center, text_radius, self._title, 0)
        
        # Artist on bottom arc  
        if self._artist:
            self._draw_curved_text_line(painter, center, text_radius, self._artist, 180)

    def _draw_curved_text_line(self, painter: QPainter, center: QPointF, radius: float, 
                              text: str, start_angle: float) -> None:
        """Draw a single line of text curved around a circle."""
        font_metrics = QFontMetrics(painter.font())
        
        # Check if text fits; if too long, truncate
        max_arc_length = math.pi * radius  # Half circle max
        text_width = font_metrics.horizontalAdvance(text)
        
        if text_width > max_arc_length and len(text) > 8:
            # Truncate with ellipsis
            while text and font_metrics.horizontalAdvance(text + "...") > max_arc_length:
                text = text[:-1]
            text += "..."
        
        if not text:
            return
            
        # Calculate angle per character
        chars = list(text)
        total_width = font_metrics.horizontalAdvance(text)
        angle_per_char = math.degrees(total_width / radius)
        
        # Calculate starting angle to center the text
        if start_angle == 0:  # Top arc
            current_angle = -angle_per_char / 2
        else:  # Bottom arc  
            current_angle = 180 - angle_per_char / 2
        
        # Draw each character
        for i, char in enumerate(chars):
            if i > 0:
                char_width = font_metrics.horizontalAdvance(chars[i-1])
                current_angle += math.degrees(char_width / radius)
            
            # Position and rotate character
            char_angle_rad = math.radians(current_angle)
            char_x = center.x() + radius * math.cos(char_angle_rad)
            char_y = center.y() + radius * math.sin(char_angle_rad)
            
            # Save painter state and apply rotation
            painter.save()
            painter.translate(char_x, char_y)
            
            # Rotate text to be upright relative to center
            if start_angle == 0:  # Top arc - text tangent to circle
                painter.rotate(current_angle + 90)
            else:  # Bottom arc - text tangent but inverted
                painter.rotate(current_angle - 90)
            
            # Draw character
            painter.drawText(QPointF(-font_metrics.horizontalAdvance(char) // 2, 0), char)
            painter.restore()

    def _create_circle_path(self, center: QPointF, radius: float) -> QPainterPath:
        """Helper to create a circular clipping path."""
        path = QPainterPath()
        path.addEllipse(center, radius, radius)
        return path

    def _on_tick(self) -> None:
        """Animation timer callback."""
        self._angle += DEGREES_PER_FRAME
        if self._angle >= 360.0:
            self._angle -= 360.0
        self.update()