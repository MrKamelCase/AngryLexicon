def tilesUsed(usedWord, location, orientation, board):
    if orientation == "horizontal":
        orient = (1, 0)
    elif orientation == "vertical":
        orient = (0, 1)
    usedTiles = ""
    for i, char in enumerate(usedWord):
        x = location[0] + orient[0] * i
        y = location[1] + orient[1] * i
        if board[(x, y)] == (".", "."):
            usedTiles += char
    return usedTiles


def tilesUsedList(plays, board):
    newPlays = list()
    for play in plays:
        usedWord, location, orientation = play[2:5]
        tiles = tilesUsed(usedWord, location, orientation, board)
        play += (tiles,)
        newPlays.append(play)
    return newPlays
