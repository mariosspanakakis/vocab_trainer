from PyQt5.QtCore import Qt, pyqtSignal, QObject
import json
from utils import get_param
from trainer import Trainer
from word import Word


class TrainerLogic(QObject):

    sig_update_word_card = pyqtSignal(dict, bool) # word, reveal
    sig_switch_menu = pyqtSignal(int) # layer index

    def __init__(self):
        super().__init__()
        self.trainer = Trainer()
        self.active_card = None

    # get a new card and display only the german meaning
    def get_new_word(self):
        self.active_card = self.trainer.draw_word()
        self.sig_update_word_card.emit(self.active_card.to_dict(), False)
        self.sig_switch_menu.emit(1)

    # reveal the spanish meaning of the active card
    def reveal_active_card(self):
        self.sig_update_word_card.emit(self.active_card.to_dict(), True)
        self.sig_switch_menu.emit(2)
    
    # update the level of the currently active card
    def reclassify_active_card(self, known: bool):
        self.trainer.reclassify_word(self.active_card, known)
        self.active_card = None
        self.save()
        self.sig_update_word_card.emit(dict(), False)
        self.sig_switch_menu.emit(0)

    # save the current vocabulary list to a JSON file
    def save(self):
        vocabulary = {}
        for key, stage in self.trainer.stages.items():
            vocabulary[key] = [word.to_dict() for word in stage]
        with open(get_param('DATA_FILE'), 'w', encoding='utf8') as file:
            json.dump(vocabulary, file, indent=4)

    # load the latest vocabulary configuration from the data file
    def load(self):
        with open(get_param('DATA_FILE'), 'r', encoding='utf8') as file:
            try:
                vocabulary = json.load(file)
                self.trainer.load_vocabulary(vocabulary)
            except json.decoder.JSONDecodeError as error:
                print(f"[ERROR]\t{error}")
