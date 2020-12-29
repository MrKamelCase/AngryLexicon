#! /usr/bin/env python3

import sqlite3
import sys


def renderBoard(gameID, dbFileName):
    """ Returns: board dictionary, board height, board width"""
    dbPath = dbFileName
    game_id = gameID

    conn = sqlite3.connect(dbPath)
    cur = conn.cursor()

    cur.execute(
        r"""SELECT width, height FROM Boards JOIN Games
        WHERE Boards.ID = Games.Board_ID AND Games.ID = ?""",
        (game_id,),
    )
    boardWidth, boardHeight = cur.fetchone()

    cur.execute(
        r"""SELECT word, location, orientation, tiles FROM events
        WHERE game_id = ? AND word IS NOT NULL""",
        (game_id,),
    )
    events = cur.fetchall()
    conn.close()

    played = dict()
    for event in events:
        word, location, orientation, tiles = event
        x = location % boardWidth
        y = location // boardWidth
        if x == 0:
            x = boardWidth
            y -= 1
        locList = [x, y]
        if orientation == "horizontal":
            locInd = 0
        elif orientation == "vertical":
            locInd = 1
        locList[locInd] -= 1
        for i in range(len(word)):
            locList[locInd] += 1
            locTup = (locList[0], locList[1])
            played[locTup] = (word[i], tiles[i])

    board = {
        (x, y): (".", ".")
        for x in range(1, boardWidth + 1)
        for y in range(1, boardHeight + 1)
    }
    board.update(played)
    return board, boardHeight, boardWidth


def printBoard(boardDict, boardHeight, boardWidth):
    for y in range(1, boardHeight + 1):
        for x in range(1, boardWidth + 1):
            print((boardDict[(x, y)][0]), end=" ")
        print()


def getModDict(gameID, dbFileName):
    """ Returns mod dictioary, (x, y) for start"""
    conn = sqlite3.connect(dbFileName)
    cur = conn.cursor()

    cur.execute(
        r"""SELECT width FROM Boards JOIN Games
        WHERE Boards.ID = Games.Board_ID AND Games.ID = ?""",
        (gameID,),
    )
    boardWidth = cur.fetchone()[0]
    cur.execute(
        r"""SELECT Location, Letter, Word FROM Modifiers JOIN Boards JOIN Games
        WHERE Modifiers.Modifier_ID = Boards.Modifier_ID
        AND Boards.ID = Games.Board_ID
        AND Games.ID = ? AND Modifiers.Star IS NULL""",
        (gameID,),
    )
    modifiers = cur.fetchall()
    modDict = dict()
    for modifier in modifiers:
        location, letter, word = modifier
        x = location % boardWidth
        y = location // boardWidth
        if x == 0:
            x = boardWidth
            y -= 1
        modDict[(x, y)] = (
            letter,
            word,
        )

    cur.execute(
        r"""SELECT Star FROM Modifiers JOIN Boards JOIN Games
        WHERE Modifiers.Modifier_ID = Boards.Modifier_ID
        AND Boards.ID = Games.Board_ID
        AND Games.ID = ? AND Modifiers.Star IS NOT NULL""",
        (gameID,),
    )
    star = cur.fetchone()[0]
    x = star % boardWidth
    y = star // boardWidth
    if x == 0:
        x = boardWidth
        y -= 1
    conn.close()
    return modDict, (x, y)


def main(path, gameNum):
    board, boardH, boardW = renderBoard(gameNum, path)
    printBoard(board, boardH, boardW)


if __name__ == "__main__":
    gameID = sys.argv[1]
    path = sys.argv[2]
    main(path, gameID)
