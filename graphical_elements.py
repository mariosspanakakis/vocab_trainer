from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QStackedWidget, QWidget, QLabel, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from utils import get_param
import stylesheets as style


class ClickableLabel(QLabel):

    clicked = pyqtSignal(str) # content

    def __init__(self, content: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.content = content
        self._active = False

        self.setFixedSize(get_param('TYPE_LABEL_W'), get_param('TYPE_LABEL_H'))
        self.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.active = False
    
    @property
    def active(self):
        return self._active
    
    @active.setter
    def active(self, set_active):
        if set_active:
            self.setStyleSheet(style.LABEL_SELECTED)
        else:
            self.setStyleSheet(style.LABEL_UNSELECTED)

    def mousePressEvent(self, event):
        self.clicked.emit(self.content)
        self.active = True