from textgenrnn import textgenrnn

fortune_bot = textgenrnn()
fortune_bot.train_from_file('fortunes_clean_dedupe.txt', num_epochs=100)
fortune_bot.save('fortunes_clean_dedupe.hdf5')