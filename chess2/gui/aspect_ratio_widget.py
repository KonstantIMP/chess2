"""
Виджет, которые поддерживает постоянное соотношение
сторон у дочернего элемента
"""
from PyQt6.QtWidgets import QWidget, QBoxLayout, QSpacerItem
from PyQt6.QtGui import QResizeEvent


class AspectRatioWidget(QWidget):
    """
    Поддерживает постоянное соотношение сторон у
    элемента child (width/height = const)
    """
    def __init__(self, child: QWidget, width: float = 1.0, height: float = 1.0):
        super(AspectRatioWidget, self).__init__()

        self.width, self.height = width, height
        self.layout = QBoxLayout(QBoxLayout.Direction.LeftToRight, self)

        self.layout.addItem(QSpacerItem(0, 0))
        self.layout.addWidget(child)
        self.layout.addItem(QSpacerItem(0, 0))


    def resizeEvent(self, event: QResizeEvent) -> None:
        new_aspect_ratio = float(event.size().width()) / event.size().height()
        prev_aspect_ratio = self.width / self.height

        widget_stretch, outer_stretch = None, None

        if new_aspect_ratio > prev_aspect_ratio:
            self.layout.setDirection(QBoxLayout.Direction.LeftToRight)
            widget_stretch = self.geometry().height() * prev_aspect_ratio
            outer_stretch = (self.geometry().width() - widget_stretch) / 2 + 0.5
        else:
            self.layout.setDirection(QBoxLayout.Direction.TopToBottom)
            widget_stretch = self.geometry().width() / prev_aspect_ratio
            outer_stretch = (self.geometry().height() - widget_stretch) / 2 + 0.5

        for i in [0, 2]:
            self.layout.setStretch(i, int(outer_stretch))
        self.layout.setStretch(1, int(widget_stretch))
