from math import floor
from utils import get_param


class Word:

    # initialise a word with its meanings, its type and its gender
    def __init__(self, es: str, de: str, type: str, 
                    gender=None, level=get_param('MAX_LEVEL')):
        self.es = es
        self.de = de
        self.type = type
        self.gender = gender
        self._level = level
        self.stage = floor(level)

    @property
    def level(self):
        return self._level
    
    @level.setter
    def level(self, value):
        value = min(value, get_param('MAX_LEVEL'))
        value = max(value, get_param('MIN_LEVEL'))
        self.stage = floor(value)
        self._level = value

    # depending on whether the word was known, update its level
    def update_level(self, known: bool):
        if known:
            self.level -= (
                self.level - get_param('MIN_LEVEL')) * get_param('LVL_DECAY')
        else:
            self.level += (
                get_param('MAX_LEVEL') - self.level) * get_param('LVL_GROWTH')
        print(f'Word level reclassified to {self.level}.')

    # generate a dictionary for displaying and saving in JSON
    def to_dict(self) -> dict:
        dictionary = {
            'de': self.de,
            'es': self.es,
            'type': self.type,
            'gender': self.gender,
            'level': round(self.level, 2)
        }
        return dictionary

    # print the spanish word an the german meaning
    def __repr__(self) -> str:
        return (self.es)