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

        self.load()

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

    # add a user-specific word to the trainer's vocabulary list
    def add_word(self, word_data):
        word = Word(es=word_data['es'],
                    de=word_data['de'],
                    type=word_data['type'])
        self.trainer.add_word(word)

    # save the current vocabulary list
    def save(self):
        with open(get_param('DATA_FILE'), 'w', encoding='utf8') as file:
            for stage in self.trainer.stages.values():
                for word in stage:
                    file.write(word.export())
            for word in self.trainer.buffer:
                file.write(word.export())

    # load the vocabulary list from the data file
    def load(self):
        with open(get_param('DATA_FILE'), 'r', encoding='utf8') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip().split(';')
                self.trainer.add_word(Word(es=line[0], de=line[1],
                                           type=line[2], level=float(line[3])))
