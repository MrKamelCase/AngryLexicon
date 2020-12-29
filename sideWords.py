from scoring import score
from tilesDict import getTiles
from locations import removeAlreadyOnBoard

tileValue = getTiles()


def goDirection(slot, direction, board, boardH, boardW):
    if direction == "r":
        xd, yd = 1, 0
    elif direction == "l":
        xd, yd = -1, 0
    elif direction == "u":
        xd, yd = 0, -1
    elif direction == "d":
        xd, yd = 0, 1
    else:
        raise ValueError("Direction must be 'r', 'l', 'u', or 'd'")
    (x, y) = slot
    if (
        x + xd == 0
        or y + yd == 0
        or x + xd > boardW
        or y + yd > boardH
        or board[(x + xd, y + yd)] == (".", ".")
    ):
        return slot
    else:
        return goDirection((x + xd, y + yd), direction, board, boardH, boardW)


def checkPath(
    word, used, path, d1, d2, board, boardH, boardW, dictionary, modDict
):
    pathIsGood = True
    scoreSides = 0
    if d1 == "l":
        key = 0
    if d1 == "u":
        key = 1
    for index, slot in enumerate(path):
        letter = word[index]
        tile = used[index]
        bSlot = goDirection(slot, d1, board, boardH, boardW)
        eSlot = goDirection(slot, d2, board, boardH, boardW)
        if bSlot == slot and eSlot == slot:
            continue
        testWord = ""
        usedWord = ""
        wordmod = 1
        path = [[]]
        for elelment in range(bSlot[key], eSlot[key] + 1):
            if elelment == slot[key]:
                testWord += letter
                usedWord += tile
                wordmod = modDict[slot][1]
                scoreSides += tileValue[tile][1] * modDict[slot][0]
                path[0].append(slot)
            elif key == 0:
                testWord += board[(elelment, slot[1])][0]
                usedTile = board[(elelment, slot[1])][1]
                usedWord += usedTile
                scoreSides += tileValue[usedTile][1]
                path[0].append((elelment, slot[1]))
            else:
                testWord += board[(slot[0], elelment)][0]
                usedTile = board[(slot[0], elelment)][1]
                usedWord += usedTile
                scoreSides += tileValue[usedTile][1]
                path[0].append((slot[0], elelment))
        scoreSides = scoreSides * wordmod
        if path != removeAlreadyOnBoard(path, board):
            scoreSides = 0
        goodWord = False
        if testWord in dictionary:
            goodWord = True
        if goodWord is False:
            pathIsGood = False
            scoreSides = 0
            break
    return pathIsGood, scoreSides


def fileToSet(dictionary):
    with open(dictionary) as file:
        data = file.read().replace("\n", " ")
    return set(data.split())


def confirmChoices(choices, board, boardH, boardW, dictionaryFile, modDict):
    confirmed = dict()
    dictionary = fileToSet(dictionaryFile)
    for word, knowledge in choices.items():
        used, horizontal, vertical = knowledge
        for path in horizontal:
            location = path[0]
            ok, scoreSides = checkPath(
                word,
                used,
                path,
                "u",
                "d",
                board,
                boardH,
                boardW,
                dictionary,
                modDict,
            )
            if ok is True:
                wordScore, usedWord = score(used, location, 0, board, modDict)
                scoreSides += wordScore
                value = confirmed.get(word, list())
                value.append(
                    (scoreSides, usedWord, location, "horizontal", scoreSides)
                )
                confirmed[word] = value
        for path in vertical:
            location = path[0]
            ok, scoreSides = checkPath(
                word,
                used,
                path,
                "l",
                "r",
                board,
                boardH,
                boardW,
                dictionary,
                modDict,
            )
            if ok is True:
                wordScore, usedWord = score(used, location, 1, board, modDict)
                scoreSides += wordScore
                value = confirmed.get(word, list())
                value.append((scoreSides, usedWord, location, "vertical"))
                confirmed[word] = value

    return confirmed
