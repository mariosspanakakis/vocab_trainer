from collections import deque
import numpy as np

from word import Word
from utils import get_param


class Trainer:

    def __init__(self):
        # define a number of stages in which the words are classified
        self.stages = {}
        for i in range(int(get_param('MAX_LEVEL'))):
            self.stages[i + 1] = deque()
        
        # define and normalize the probabilities for each stage to be picked when drawing vocabulary
        self.stage_weights = np.logspace(0, 1, int(get_param('MAX_LEVEL')))
        self.stage_weights /= np.sum(self.stage_weights)

    # add a word to the list of known words
    def add_word(self, word: Word):
        self.stages[word.stage].appendleft(word)

    # draw the next word from a random stage
    def draw_word(self):
        stage = np.random.choice(range(1, len(self.stages) + 1), p=self.stage_weights)
        word = None
        while not word:
            if self.stages[stage]:
                word = self.stages[stage].pop()         
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
    def reclassify_word(self, word: Word, known: bool):
        word.update_level(known)
        self.stages[word.stage].appendleft(word)

        for key, stage in self.stages.items():
            print(f'Stage {key}: {stage}')