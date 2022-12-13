from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from utils import get_param
import stylesheets as style


class ClickableLabel(QLabel):

    clicked = pyqtSignal(int) # id

    def __init__(self, content: str, id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.content = content
        self.id = id
        self._active = False

        self.setText(content)
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
        self.clicked.emit(self.id)


class MenuOptions(QWidget):

    def __init__(self, options: list, horizontal=True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.options = options
        self.labels = {}

        self.active_id = None

        layout = QHBoxLayout(self) if horizontal else QVBoxLayout(self)
        self.setLayout(layout)

        for i, option in enumerate(self.options):
            click_label = ClickableLabel(content=option, id=i)
            click_label.clicked.connect(self.switch_active)
            self.labels[i] = click_label
            layout.addWidget(click_label)

    def switch_active(self, id):
        self.active_id = id
        for label in self.labels.values():
            label.active = False
        self.labels[id].active = True