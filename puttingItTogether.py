from renderBoard import renderBoard
from renderBoard import getModDict
from anagrams import getAnagrams
from sideWords import confirmChoices
from orderByPts import orderByPoints
from startingWord import getStartingWord
from tilesUsed import tilesUsedList
from time import perf_counter

dictionary = "WWFWords.txt"


def getTopWord(board, boardH, boardW, modDict, star, tiles, file=dictionary):
    """Returns top scoring words.
    (word, tiles on board, starting position, orientation, tiles from rack)
    """
    start = getStartingWord(modDict, star, board, boardW, tiles, dictionary)
    if start is not None:
        return start
    else:
        choices = getAnagrams(tiles, board, boardH, boardW, dictionary)
        confirmedChoices = confirmChoices(
            choices, board, boardH, boardW, dictionary, modDict
        )
        playsByPt = orderByPoints(confirmedChoices)
        final = tilesUsedList(playsByPt[:1], board)
        return final[0]


if __name__ == "__main__":
    t1 = perf_counter()
    dictionary = "WWFWords.txt"
    tiles = "astekgo"
    gameID = 1
    dbFileName = "TestScrabble.sqlite"
    print("Rendering Board")
    board, boardH, boardW = renderBoard(gameID, dbFileName)
    modDict, star = getModDict(gameID, dbFileName)
    print("Checking Game Status")
    start = getStartingWord(modDict, star, board, boardW, tiles, dictionary)
    if start is not None:
        print(start)
    else:
        print("Finding Anagrams")
        choices = getAnagrams(tiles, board, boardH, boardW, dictionary)
        print("Found", len(choices.keys()), "Possible Anagrams")
        print("Confirming Placement")
        confirmedChoices = confirmChoices(
            choices, board, boardH, boardW, dictionary, modDict
        )
        print("Narrowed to ", len(confirmedChoices.keys()))
        print("Sorting by point value")
        playsByPt = orderByPoints(confirmedChoices)
        final = tilesUsedList(playsByPt, board)
        print(final)
    t2 = perf_counter()

    print(t2 - t1)
