def orderByPoints(dictionary):
    dictionaryAsList = list()
    for option in dictionary.items():
        word, plays = option
        for play in plays:
            play = (play[0],) + (word,) + play[1:4]
            dictionaryAsList.append(play)
    dictionaryAsList.sort(reverse=True)
    return dictionaryAsList
