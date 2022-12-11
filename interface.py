from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QStackedWidget, QWidget, QLabel, QPushButton
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QHBoxLayout
from graphical_elements import ClickableLabel
from utils import get_param
import stylesheets as style

# &6o$w0%q95k3p7ts


class Interface(QWidget):

    sig_quit_application = pyqtSignal()
    sig_get_new_word = pyqtSignal()
    sig_reveal_card = pyqtSignal()
    sig_rate_card = pyqtSignal(bool) # known

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Vokabeljau')

        # generate widgets that contain the different interface layers
        self.wid_menu = QWidget()
        self.wid_train = QWidget()
        self.wid_add = QWidget()
        self.wid_manage = QWidget()
        self.wid_settings = QWidget()
        # add the widgets to the stacked layout
        self.stack = QStackedWidget()
        self.stack.addWidget(self.wid_menu)
        self.stack.addWidget(self.wid_train)
        self.stack.addWidget(self.wid_add)
        self.stack.addWidget(self.wid_manage)
        self.stack.addWidget(self.wid_settings)

        self.create_menu_widget()
        self.create_train_widget()
        self.create_add_widget()

        self.main_vbox = QVBoxLayout()
        self.main_vbox.addWidget(self.stack)
        self.setLayout(self.main_vbox)
    
    def create_menu_widget(self):
        vbox = QVBoxLayout(self)

        label = QLabel('Hauptmenü')
        label.setAlignment(Qt.AlignCenter)
        self.btn_train = QPushButton('Trainieren', self)
        self.btn_train.clicked.connect(
            lambda: self.switch_context(self.wid_train))
        self.btn_add = QPushButton('Vokabel hinzufügen', self)
        self.btn_add.clicked.connect(
            lambda: self.switch_context(self.wid_add))
        self.btn_manage = QPushButton('Vokabeln verwalten', self)
        self.btn_settings = QPushButton('Einstellungen', self)
        self.btn_quit = QPushButton('Schließen', self)
        self.btn_quit.clicked.connect(self.sig_quit_application.emit)

        vbox.addWidget(label)
        vbox.addWidget(self.btn_train)
        vbox.addWidget(self.btn_add)
        vbox.addWidget(self.btn_manage)
        vbox.addWidget(self.btn_settings)
        vbox.addWidget(self.btn_quit)

        self.wid_menu.setLayout(vbox)

    def create_train_widget(self):
        vbox = QVBoxLayout(self)

        label = QLabel('Vokabeltrainer')
        label.setAlignment(Qt.AlignCenter)

        self.btn_menu = QPushButton('Hauptmenü', self)
        self.btn_menu.clicked.connect(
            lambda: self.switch_context(self.wid_menu))
        
        # german word card
        layout = QVBoxLayout()
        self.lbl_word_de = QLabel('', self)
        self.lbl_word_de.setAlignment(Qt.AlignCenter)
        self.lbl_word_de.setStyleSheet(style.WORD_CARD)
        self.lbl_word_de.setFixedSize(
            get_param("WORD_CARD_W"), get_param("WORD_CARD_H"))
        # spanish word card
        self.lbl_word_es = QLabel('', self)
        self.lbl_word_es.setAlignment(Qt.AlignCenter)
        self.lbl_word_es.setStyleSheet(style.WORD_CARD)
        self.lbl_word_es.setFixedSize(
            get_param("WORD_CARD_W"), get_param("WORD_CARD_H"))
        layout.addWidget(self.lbl_word_de)
        layout.addWidget(self.lbl_word_es)

        # buttons to interact with the word card
        self.stack_word_options = QStackedWidget()
        self.get_card_widget = QWidget()
        self.btn_get_card = QPushButton('Wortkarte ziehen')
        hbox = QHBoxLayout(self.get_card_widget)
        hbox.addWidget(self.btn_get_card)
        self.get_card_widget.setLayout(hbox)
        self.btn_get_card.clicked.connect(
            self.sig_get_new_word.emit)
        self.show_card_widget = QWidget()
        hbox = QHBoxLayout(self.show_card_widget)
        self.btn_show_word = QPushButton('Umdrehen', self)
        self.btn_show_word.clicked.connect(
            self.sig_reveal_card.emit)
        hbox.addWidget(self.btn_show_word)
        self.show_card_widget.setLayout(hbox)
        self.select_answer_widget = QWidget()
        hbox = QHBoxLayout(self.select_answer_widget)
        self.btn_word_known = QPushButton('Ja', self)
        self.btn_word_known.clicked.connect(
            lambda: self.rate_word_card(known=True))
        self.btn_word_unknown = QPushButton('Nein', self)
        self.btn_word_unknown.clicked.connect(
            lambda: self.rate_word_card(known=False))
        hbox.addWidget(self.btn_word_known)
        hbox.addWidget(self.btn_word_unknown)
        self.select_answer_widget.setLayout(hbox)
        self.stack_word_options.addWidget(self.get_card_widget)
        self.stack_word_options.addWidget(self.show_card_widget)
        self.stack_word_options.addWidget(self.select_answer_widget)

        vbox.addWidget(label)
        vbox.addLayout(layout)
        vbox.addWidget(self.stack_word_options)
        vbox.addWidget(self.btn_menu)

        self.wid_train.setLayout(vbox)

    def create_manage_widget(self):
        pass

    def create_add_widget(self):
        layout = QVBoxLayout(self)
        self.wid_add.setLayout(layout)

        type_layout = QHBoxLayout()
        options = ['noun', 'verb', 'adjective', 'expression']
        self.type_options = {}
        for option in options:
            click_label = ClickableLabel(content=option)
            click_label.clicked.connect(
                self.deactivate_type_options)
            click_label.setText(option)
            type_layout.addWidget(click_label)
            self.type_options[click_label.content] = click_label

        self.edt_add_de = QLineEdit(self)
        self.edt_add_de.setPlaceholderText('DE')
        self.edt_add_es = QLineEdit(self)
        self.edt_add_es.setPlaceholderText('ES')

        self.btn_add_confirm = QPushButton('Hinzufügen', self)
        
        layout.addLayout(type_layout)
        layout.addWidget(self.edt_add_de)
        layout.addWidget(self.edt_add_es)
        layout.addWidget(self.btn_add_confirm)

    # switch between the menus
    def switch_context(self, widget: QWidget):
        self.stack.setCurrentWidget(widget)

    # update the displayed word(s)
    def update_word_card(self, word: dict, reveal: bool):
        if not word:
            self.lbl_word_de.setText('')
            self.lbl_word_es.setText('')
        else:
            self.lbl_word_de.setText(word['de'])
            if reveal:
                self.lbl_word_es.setText(word['es'])

    # switch the word menu layer
    def switch_train_menu(self, index: int):
        self.stack_word_options.setCurrentIndex(index)

    # rate the currently active word
    def rate_word_card(self, known):
        self.sig_rate_card.emit(known)

    # unhighlight all non-selected type option labels
    def deactivate_type_options(self):
        for click_label in self.type_options.values():
            click_label.active = False