from PyQt5.QtWidgets import QApplication
from trainer_logic import TrainerLogic
from interface import Interface


class Application(QApplication):

    def __init__(self, argv):
        super().__init__(argv)

        self.trainer_logic = TrainerLogic()
        self.interface = Interface()

        self.connect_signals()

    def connect_signals(self):
        self.interface.sig_quit_application.connect(
            self.quit)
        # frontend -> backend
        self.interface.sig_get_new_word.connect(
            self.trainer_logic.get_new_word)
        self.interface.sig_reveal_card.connect(
            self.trainer_logic.reveal_active_card)
        self.interface.sig_rate_card.connect(
            self.trainer_logic.reclassify_active_card)
        self.interface.sig_add_word.connect(
            self.trainer_logic.add_word)
        # backend -> frontend
        self.trainer_logic.sig_update_word_card.connect(
            self.interface.update_word_card)
        self.trainer_logic.sig_switch_menu.connect(
            self.interface.switch_train_menu)

    def start(self):
        self.interface.show()