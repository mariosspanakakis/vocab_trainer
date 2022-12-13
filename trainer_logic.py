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

        # add basic words for debugging purposes
        words = [
            ['hablar', 'sprechen', 'v'],
            ['ir', 'gehen', 'v'],
            ['decir', 'sagen', 'v'],
            ['llegar', 'kommen', 'v'],
            ['barco', 'Schiff', 'n'],
            ['nuevo', 'neu', 'a']
        ]
        for word in words:
            self.trainer.add_word(Word(es=word[0], de=word[1], type=word[2]))

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

    # save the current vocabulary list
    def save(self):
        with open(get_param('DATA_FILE'), 'w') as file:
            for stage in self.trainer.stages.values():
                for word in stage:
                    file.write(word.export())
            for word in self.trainer.buffer:
                file.write(word.export())

    # load the vocabulary list from the data file
    def load(self):
        with open(get_param('DATA_FILE'), 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip().split(',')
                self.trainer.add_word(Word(es=line[0], de=line[1],
                                           type=line[2], level=float(line[3])))
