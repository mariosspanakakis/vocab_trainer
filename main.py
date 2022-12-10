import sys
from application import Application
"""from trainer import Trainer
from word import Word


trainer = Trainer()

words = [
    ['hablar', 'sprechen', 'v'],
    ['venir', 'gehen', 'v'],
    ['decir', 'sagen', 'v'],
    ['llegar', 'kommen', 'v'],
]

for word in words:
    trainer.add_word(Word(es=word[0], de=word[1], type=word[2]))

while 1:
    input(f'\nHit enter to draw a new word.\n')
    word = trainer.draw_word()

    user_input = input(f'Do you know this word? [y/n]')
    if user_input == 'y':
        trainer.reclassify_word(word, known=True)
    else:
        trainer.reclassify_word(word, known=False)"""


if __name__ == '__main__':
    def hook(type_, value, traceback):
        print(type_)
        print(traceback)
    sys.__excepthook__ = hook

    app = Application(sys.argv)
    app.start()

    sys.exit(app.exec())