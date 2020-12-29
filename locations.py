import sys


def findFit(locations, slot, orient, board, boardH, boardW):
    boardHeight = boardH
    boardWidth = boardW
    x = slot[0]
    y = slot[1]
    ox = orient[0]
    oy = orient[1]
    if len(locations) == 0:
        newLocs = [[(x, y)]]
    else:
        newLocs = list()
        for location in locations:
            newLoc = location.copy()
            lastLoc = newLoc[-1]
            if lastLoc == ("*", "*") and x == "*" and y == "*":
                if len(newLoc) < boardHeight or len(newLoc) < boardWidth:
                    newLoc.append(("*", "*"))
            elif lastLoc == ("*", "*"):
                for i in range(1, len(newLoc) + 1):
                    newLoc.remove(("*", "*"))
                    xNew = x - (ox * i)
                    yNew = y - (oy * i)
                    if (
                        xNew == 0
                        or yNew == 0
                        or board[(xNew, yNew)] != (".", ".")
                    ):
                        newLoc = list()
                        break
                    else:
                        newLoc.append((x - (ox * i), y - (oy * i)))
                newLoc.append((x, y))
                newLoc.sort()
            else:
                (x0, y0) = lastLoc
                xNew = x0 + ox
                yNew = y0 + oy
                if (
                    x == "*"
                    and y == "*"
                    and xNew <= boardWidth
                    and yNew <= boardHeight
                    and board[(xNew, yNew)] == (".", ".")
                ):
                    newLoc.append((xNew, yNew))
                if xNew == x and yNew == y:
                    newLoc.append((x, y))
            if len(newLoc) > len(location):
                newLocs.append(newLoc)
    cleanNewLocs = list()
    for each in newLocs:
        if each not in cleanNewLocs:
            cleanNewLocs.append(each)
    return cleanNewLocs


def checkBegEnd(path, board, boardH, boardW):
    if path[0] == ("*", "*"):
        return True
    boardHeight = boardH
    boardWidth = boardW
    firstSlot = path[0]
    (xf, yf) = firstSlot
    lastSlot = path[-1]
    (xl, yl) = lastSlot
    if xf == xl:
        ox, oy = 0, 1
    elif yf == yl:
        ox, oy = 1, 0

    before = False
    xb = xf - ox
    yb = yf - oy
    if xb == 0 or yb == 0:
        before = True
    elif board[(xb, yb)] == (".", "."):
        before = True

    after = False
    xa = xl + ox
    ya = yl + oy
    if xa > boardWidth or ya > boardHeight:
        after = True
    elif board[(xa, ya)] == (".", "."):
        after = True

    if before is True and after is True:
        return True
    else:
        return False


def removeUnhooked(word, paths):
    unhooked = [("*", "*") for i in range(len(word))]
    try:
        paths.remove(unhooked)
    except ValueError:
        pass
    return paths


def removeAlreadyOnBoard(paths, board):
    newPaths = list()
    for path in paths:
        new = False
        for slot in path:
            if board[slot] == (".", "."):
                new = True
        if new is True:
            newPaths.append(path)
    return newPaths


def main(locations, slot, orient, board, boardH, boardW):
    print(findFit(locations, slot, orient, board, boardH, boardW))


if __name__ == "__main__":
    locations = sys.argv[1]
    slot = sys.argv[2]
    orient = sys.argv[3]
    board = sys.argv[4]
    boardH = sys.argv[5]
    boardW = sys.argv[6]
    main(locations, slot, orient, board, boardH, boardW)
