from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from puttingItTogether import getTopWord

app = FastAPI()


class BoardBasic(BaseModel):
    boardHeight: int
    boardWidth: int
    starJSON: List[int]


class Body(BaseModel):
    board: Dict[str, List[str]]
    modJSON: Dict[str, List[int]]
    boardInfo: BoardBasic
    tiles: str


def stringToTuple(string: str):
    values = tuple()
    for element in string.split(","):
        try:
            values += (int(element),)
        except ValueError:
            values += (element,)
    return values


def updateStructure(jsonDict: dict):
    newDict = dict()
    for key, value in jsonDict.items():
        newkey = stringToTuple(key)
        newDict[newkey] = tuple(value)
    return newDict


@app.post("/")
async def boardInfo(body: Body):
    boardDict = updateStructure(body.board)
    modDict = updateStructure(body.modJSON)
    star = tuple(body.boardInfo.starJSON)
    result = getTopWord(
        boardDict,
        body.boardInfo.boardHeight,
        body.boardInfo.boardWidth,
        modDict,
        star,
        body.tiles,
    )
    # pt, word, tilesOnBoard, location, orientation, tilesUsed = result
    return {"result": result}
