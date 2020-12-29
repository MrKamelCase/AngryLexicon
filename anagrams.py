from locations import findFit
from locations import checkBegEnd
from locations import removeUnhooked
from locations import removeAlreadyOnBoard


def getAnagrams(tiles, board, boardH, boardW, dictionary):
    bbylet = dict()
    for coordinate, letterTile in board.items():
        letter = letterTile[0]
        if letter == ".":
            continue
        bbylet[letter] = bbylet.get(letter, []) + [coordinate]

    with open(dictionary) as dictionary:
        choices = dict()
        for line in dictionary:
            rack = list(tiles)
            word = line.lower().strip()
            spelled = str()
            used = str()
            locationsH = list()
            locationsV = list()
            for index, char in enumerate(word):
                if char in bbylet.keys() and char in rack:
                    rack.remove(char)
                    spelled += char
                    used += char
                    subLocH = list()
                    subLocV = list()
                    for slot in bbylet[char]:
                        subLocH.extend(
                            findFit(
                                locationsH, slot, (1, 0), board, boardH, boardW
                            )
                        )
                        subLocV.extend(
                            findFit(
                                locationsV, slot, (0, 1), board, boardH, boardW
                            )
                        )
                    subLocH.extend(
                        findFit(
                            locationsH,
                            ("*", "*"),
                            (1, 0),
                            board,
                            boardH,
                            boardW,
                        )
                    )
                    subLocV.extend(
                        findFit(
                            locationsV,
                            ("*", "*"),
                            (0, 1),
                            board,
                            boardH,
                            boardW,
                        )
                    )
                    locationsH = subLocH.copy()
                    locationsV = subLocV.copy()
                elif char in bbylet.keys():
                    spelled += char
                    used += char
                    subLocH = list()
                    subLocV = list()
                    for slot in bbylet[char]:
                        subLocH.extend(
                            findFit(
                                locationsH, slot, (1, 0), board, boardH, boardW
                            )
                        )
                        subLocV.extend(
                            findFit(
                                locationsV, slot, (0, 1), board, boardH, boardW
                            )
                        )
                    locationsH = subLocH.copy()
                    locationsV = subLocV.copy()
                elif char in rack:
                    rack.remove(char)
                    spelled += char
                    used += char
                    locationsH = findFit(
                        locationsH, ("*", "*"), (1, 0), board, boardH, boardW
                    )
                    locationsV = findFit(
                        locationsV, ("*", "*"), (0, 1), board, boardH, boardW
                    )
                elif "*" in rack:
                    rack.remove("*")
                    spelled += char
                    used += "*"
                    locationsH = findFit(
                        locationsH, ("*", "*"), (1, 0), board, boardH, boardW
                    )
                    locationsV = findFit(
                        locationsV, ("*", "*"), (0, 1), board, boardH, boardW
                    )
                else:
                    spelled = ""
                    used = ""
                    locationsH = list()
                    locationsV = list()
                    break
                tempLoc = list()
                for path in locationsH:
                    if index + 1 == len(path):
                        tempLoc.append(path)
                locationsH = tempLoc.copy()
                tempLoc = list()
                for path in locationsV:
                    if index + 1 == len(path):
                        tempLoc.append(path)
                locationsV = tempLoc.copy()
                if len(locationsH) == 0 and len(locationsV) == 0:
                    spelled = ""
                    used = ""
                    break
            if len(spelled) == len(word):
                removeUnhooked(word, locationsV)
                removeUnhooked(word, locationsH)
                locationsV = removeAlreadyOnBoard(locationsV, board)
                locationsH = removeAlreadyOnBoard(locationsH, board)
                tempLoc = list()
                for path in locationsH:
                    if checkBegEnd(path, board, boardH, boardW) is True:
                        tempLoc.append(path)
                locationsH = tempLoc.copy()
                tempLoc = list()
                for path in locationsV:
                    if checkBegEnd(path, board, boardH, boardW) is True:
                        tempLoc.append(path)
                locationsV = tempLoc.copy()
                if len(locationsH) > 0 or len(locationsV) > 0:
                    choices[spelled] = (used, locationsH, locationsV)

    return choices
