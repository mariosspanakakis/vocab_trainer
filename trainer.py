from collections import deque
import numpy as np

from word import Word
from utils import get_param


class Trainer:

    def __init__(self):
        # define a number of empty stages in which the words are classified
        self.stages = {}
        for i in range(int(get_param('MAX_LEVEL'))):
            self.stages[i + 1] = []
        
        # define and normalize the probabilities for each stage to be picked
        self.weights = np.logspace(0, 1, int(get_param('MAX_LEVEL')))
        self.weights /= np.sum(self.weights)

        # add basic words for debugging purposes
        """words = [
            ['hablar', 'sprechen', 'v'],
            ['ir', 'gehen', 'v'],
            ['decir', 'sagen', 'v'],
            ['llegar', 'kommen', 'v'],
        ]
        for word in words:
            self.add_word(Word(es=word[0], de=word[1], type=word[2]))"""

    # add a word to the list of known words
    def add_word(self, word: Word) -> None:
        self.stages[word.stage].append(word)

    # draw the next word from a random stage
    def draw_word(self) -> Word:
        stage = np.random.choice(range(1, len(self.stages) + 1), p=self.weights)
        word = None
        while not word:
            if self.stages[stage]:
                word = self.stages[stage].pop(0)         
                print(f"Took word from stage {stage}: {word}")
            # if the stage is empty, go downwards until finding a word
            else:
                if stage == 1:
                    stage = 5
                else:
                    stage -= 1
                print(f"Went to stage {stage}.")
        return word
    
    # update the word status and put it into the corresponding stage
    def reclassify_word(self, word: Word, known: bool) -> None:
        word.update_level(known)
        self.stages[word.stage].append(word)

        for key, stage in self.stages.items():
            print(f'Stage {key}: {stage}')

    # load the given vocabulary into the trainer's stages
    def load_vocabulary(self, vocabulary: dict):
        for stage in vocabulary.values():
            for word in stage:
                self.add_word(Word(es=word['es'],
                                   de=word['de'],
                                   type=word['type'],
                                   gender=word['gender'],
                                   level=word['level']))