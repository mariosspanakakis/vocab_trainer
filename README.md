# Vocabulary Trainer

A simple vocabulary trainer based on ```PyQt5```. Supply your own vocab via the application or by editing ```user_data/vocabulary.csv```.

### Word Staging

Each word is assigned a level between ```0.0``` and ```5.0``` that describes how difficult it is for the user. If the user cannot remember the translation, the word level is increased. If he is familiar with the word, the difficulty level is decreased. The higher the word level, the more frequently it will be picked. The parameters for level handling can be adjusted in ```parameters.json```. The word level decrease factor ```LVL_DECAY``` should be set smaller than the level increase factor ```LVL_GROWTH``` in order to make sure that words are not excluded prematurely.

### Word Buffer

To avoid words being picked repeatedly, there is a buffer of fixed length ```BUFFER_LENGTH``` that retains words before passing them to the staging area.