def getBlankBoard():
    blankBoard = {
        (x, y): (".", ".") for x in range(1, 16) for y in range(1, 16)
    }
    return blankBoard
