from tilesDict import getTiles

tileValue = getTiles()


def score(word, location, orientation, board, modDict):
    # Orientation of 1 is vertical
    # Orientation of 0 is horizontal
    if orientation == 1:
        key = (0, 1)
    if orientation == 0:
        key = (1, 0)
    score = int()
    wordMod = 1
    used = ""
    for index, char in enumerate(word):
        x = location[0] + key[0] * index
        y = location[1] + key[1] * index
        if board[(x, y)] != (".", "."):
            char = board[(x, y)][1]
            tileMod = 1
            wordMod *= 1
        else:
            tileMod = modDict[(x, y)][0]
            wordMod *= modDict[(x, y)][1]
        tileVal = tileValue[char][1]
        score += tileVal * tileMod
        used += char
    score = score * wordMod
    return score, used
