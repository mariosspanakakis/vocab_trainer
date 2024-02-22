# Vocabulary Trainer

A simple vocabulary trainer based on ```PyQt5```. You can easily customize your vocabulary either within the application or by editing the ```user_data/vocabulary.csv``` file.

### Word Staging

Each word in your vocabulary is assigned a difficulty level ranging from ```0.0``` to ```5.0```, indicating its challenge for you. When you struggle to recall a translation, the word's difficulty level increases. Conversely, if you successfully remember it, the difficulty level decreases. This dynamic system ensures that words you find challenging are presented more frequently, which is known as the spaced-repetition learning method. You can fine-tune the parameters for managing word levels in the ```parameters.json``` file. It is essential to set the word level decrease factor ```LVL_DECAY``` smaller than the level increase factor ```LVL_GROWTH``` to prevent prematurely excluding words from your learning process.

### Word Buffer

To prevent repetitive selection of words, there's a buffer with a fixed length ```BUFFER_LENGTH``` that temporarily stores words before they are introduced into the staging area.
