# Vocabulary Trainer

A simple vocabulary trainer based on ´´´PyQt5´´´. Supply your own vocab via the application or by editing ```user_data/vocabulary.csv´´´.

### Word Staging

Each word is assigned a level that describes its how challenging it is to the user. If the user does not remember the translation, the word level is increased. If he is familiar to the word, the word level is decreased. Words with a level lower than ´´´1´´´ are assumed to be known and will not further be tested.