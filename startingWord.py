from anWithWild import getAnagrams
from scoring import score


def getStartingWord(modDict, star, board, boardW, rack, dictionary):
    boardWidth = boardW
    star = star
    if board[star] != (".", "."):
        return None
    possible = getAnagrams(rack, dictionary)
    overallHighestScore = 0
    play = list()
    for word, used in possible.items():
        highestScore = 0
        positions = list()
        usedlen = len(used)
        for i in range(usedlen):
            x0 = star[0] + 1 - usedlen + i
            xe = x0 + usedlen - 1
            y = star[1]
            if x0 < 1:
                continue
            if xe > boardWidth:
                break
            posscore = score(used, (x0, y), 0, board, modDict)[0]
            if posscore == highestScore:
                positions.append((x0, y))
            elif posscore > highestScore:
                highestScore = posscore
                positions = [(x0, y)]
        if highestScore == overallHighestScore:
            for position in positions:
                play.append(
                    (
                        overallHighestScore,
                        word,
                        used,
                        position,
                        "horizontal",
                        used,
                    )
                )
        if highestScore > overallHighestScore:
            overallHighestScore = highestScore
            play = list()
            for position in positions:
                play = [
                    (
                        overallHighestScore,
                        word,
                        used,
                        position,
                        "horizontal",
                        used,
                    )
                ]

    return play
