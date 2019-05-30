from main import Piece, Board
from random import randint
# ======================== Class Player =======================================


class Player:
    # student do not allow to change two first functions
    def __init__(self, str_name):
        self.str = str_name

    def __str__(self):
        return self.str

    # Student MUST implement this function
    # The return value should be a move that is denoted by:
        # piece: selected piece
        # (row, col): new position of selected piece
    def next_move(self, state):
        currentState = state
        if self.str == "black":
            # find next moves
            nextMoves = possibleNextMoves(state, "black")
            if nextMoves == list():
                return False
            bestMove = None
            playerMaxScore = -1000000
            opponentMinScore = 1000000
            for move in nextMoves:
                # print("DEBUG: " + str(move[0][0]) + " to " + str(move[0][1]))
                if playerMaxScore > move[1]:
                    continue
                if playerMaxScore == move[1]:
                    r = randint(0, 100)
                    if r > 70:
                        # print("HAHA SKIP " + str(move[0][0]) + str(move[0][1]))
                        bestMove = move
                        playerMaxScore = move[1]
                        continue
                    else:
                        pass
                nextState = doMove((move[0][0], move[0][1]), currentState)
                opponentMoves = possibleNextMoves(nextState, "red")
                # find opponent best move
                for oppMove in opponentMoves:
                    if opponentMinScore <= oppMove[1]:
                        continue
                    elif opponentMinScore > oppMove[1]:
                        opponentMinScore = oppMove[1]
                        bestMove = move
                        playerMaxScore = move[1]

        if self.str == "red":
            # find next moves
            nextMoves = possibleNextMoves(state, "red")
            if nextMoves == list():
                return None
            bestMove = None
            playerMaxScore = -1000000
            opponentMinScore = 1000000
            for move in nextMoves:
                if playerMaxScore > move[1]:
                    continue
                if playerMaxScore == move[1]:
                    r = randint(0, 100)
                    if r > 70:
                        # print("HAHA SKIP " + str(move[0][0]) + str(move[0][1]))
                        bestMove = move
                        playerMaxScore = move[1]
                        continue
                    else:
                        pass
                nextState = doMove((move[0][0], move[0][1]), currentState)
                opponentMoves = possibleNextMoves(nextState, "black")
                # find opponent best move
                for oppMove in opponentMoves:
                    if opponentMinScore <= oppMove[1]:
                        continue
                    elif opponentMinScore > oppMove[1]:
                        opponentMinScore = oppMove[1]
                        bestMove = move
                        playerMaxScore = move[1]

        return bestMove[0][0], bestMove[0][1]


# CONSTANTS:
Voi = 'Voi'
SuTu = 'SuTu'
Ho = 'Ho'
Bao = 'Bao'
Soi = 'Soi'
Cho = 'Cho'
Meo = 'Meo'
Chuot = 'Chuot'
blackWinPosition = (1, 4)
redWinPosition = (9, 4)
trapPosition = [(1, 3), (1, 5), (2, 4), (9, 3), (9, 5), (8, 4)]
waterPosition = [(4, 2), (4, 3), (4, 5), (4, 6), (5, 2), (5, 3), (5, 5), (5, 6), (6, 2), (6, 3), (6, 5), (6, 6)]

pieceScore = {
    Voi: 8,
    SuTu: 7,
    Ho: 6,
    Bao: 5,
    Soi: 4,
    Cho: 3,
    Meo: 2,
    Chuot: 1,
}


# return a list of possible next state
def possibleNextMoves(state, side):
    list_pieces = {}
    if side == "black":
        list_pieces = {
            "player": state.list_black,
            "opponent": state.list_red
        }
    elif side == "red":
        list_pieces = {
            "player": state.list_red,
            "opponent": state.list_black
        }
    
    currentScore = evalute(state, side)
    nextMoves = []

    for piece in list_pieces.get('player'):
        pieceType = piece.type
        # print(pieceType + ":")
        # move up
        nextScore = currentScore
        nextPos = (piece.position[0] + 1, piece.position[1])
        # check special moves
        if nextPos in waterPosition:    
            if pieceType == SuTu or pieceType == Ho:
                # jump up 4
                nextPos = (piece.position[0] + 4, piece.position[1])
            elif pieceType == Bao:
                # cant jump that far
                continue
            elif pieceType == Meo:
                # Meo cant swim
                continue

        captureScore = checkNextPos(nextPos, list_pieces, piece, pieceType)

        if captureScore is not None:
            # can go there
            if nextPos in trapPosition:
                nextScore -= pieceScore.get(pieceType)
            elif nextPos in waterPosition:
                nextScore -= pieceScore.get(pieceType) / 2
            else:
                # nextScore not change
                pass
            nextScore += captureScore
            # print(str(piece) + " to (" + str(nextPos[0]) + "," + str(nextPos[1])+ "), score: " + str(nextScore))
            nextMoves.append(((piece, nextPos), nextScore))
        

        # move down
        nextScore = currentScore
        nextPos = (piece.position[0] - 1, piece.position[1])
        # check special moves
        if nextPos in waterPosition:
            if pieceType == SuTu or pieceType == Ho:
                # jump down 4
                nextPos = (piece.position[0] - 4, piece.position[1])
            elif pieceType == Bao:
                # cant jump that far
                continue
            elif pieceType == Meo:
                # Meo cant swim
                continue

        captureScore = checkNextPos(nextPos, list_pieces, piece, pieceType)

        if captureScore is not None:
            # can go there
            if nextPos in trapPosition:
                nextScore -= pieceScore.get(pieceType)
            elif nextPos in waterPosition:
                nextScore -= pieceScore.get(pieceType) / 2
            else:
                # nextScore not change
                pass
            nextScore += captureScore
            # print(str(piece) + " to (" + str(nextPos[0]) + "," + str(nextPos[1])+ "), score: " + str(nextScore))
            nextMoves.append(((piece, nextPos), nextScore))

        # move left
        nextScore = currentScore
        nextPos = (piece.position[0], piece.position[1] - 1)
        # check special moves
        if nextPos in waterPosition:
            if pieceType == SuTu or pieceType == Ho:
                # jump left 3
                nextPos = (piece.position[0], piece.position[1] - 3)
            elif pieceType == Bao:
                # jump left 3
                nextPos = (piece.position[0], piece.position[1] - 3)
            elif pieceType == Meo:
                # Meo cant swim
                continue

        captureScore = checkNextPos(nextPos, list_pieces, piece, pieceType)

        if captureScore is not None:
            # can go there
            if nextPos in trapPosition:
                nextScore -= pieceScore.get(pieceType)
            elif nextPos in waterPosition:
                nextScore -= pieceScore.get(pieceType) / 2
            else:
                # nextScore not change
                pass
            nextScore += captureScore
            # print(str(piece) + " to (" + str(nextPos[0]) + "," + str(nextPos[1])+ "), score: " + str(nextScore))
            nextMoves.append(((piece, nextPos), nextScore))

        # move right
        nextScore = currentScore
        nextPos = (piece.position[0], piece.position[1] + 1)
        # check special moves
        if nextPos in waterPosition:
            if pieceType == SuTu or pieceType == Ho:
                # jump left 3
                nextPos = (piece.position[0], piece.position[1] + 3)
            elif pieceType == Bao:
                # jump left 3
                nextPos = (piece.position[0], piece.position[1] + 3)
            elif pieceType == Meo:
                # Meo cant swim
                continue

        captureScore = checkNextPos(nextPos, list_pieces, piece, pieceType)

        if captureScore is not None:
            # can go there
            if nextPos in trapPosition:
                nextScore -= pieceScore.get(pieceType)
            elif nextPos in waterPosition:
                nextScore -= pieceScore.get(pieceType) / 2
            else:
                # nextScore not change
                pass
            nextScore += captureScore
            # print(str(piece) + " to (" + str(nextPos[0]) + "," + str(nextPos[1])+ "), score: " + str(nextScore))
            nextMoves.append(((piece, nextPos), nextScore))
    
    return nextMoves


def checkNextPos(nextPos, list_pieces, piece, pieceType):
    if not inRange(nextPos):
        # print('not in range: ' + str(nextPos))
        return None
    # check if nextPos have other player's piece
    invalidMove = False
    for otherPiece in list_pieces.get('player'):
        if nextPos == otherPiece.position:
            # invalid moves
            invalidMove = True
            return None
    
    # check if capture any opponent's piece
    captureScore = 0

    for otherPiece in list_pieces.get('opponent'):
        if nextPos == otherPiece.position:
            # check if capturable
            if piece.position in waterPosition: # check if piece in water
                if otherPiece.position in waterPosition and pieceScore.get(pieceType) >= pieceScore.get(otherPiece.type):# check if other piece in water, still can capture
                    captureScore = pieceScore.get(otherPiece.type)
                    break
                return None
            elif otherPiece.position in waterPosition:# check if other piece in water
                return None
            elif otherPiece.position in trapPosition: # check if other piece in trap
                captureScore = pieceScore.get(otherPiece.type)
                break
            elif pieceType == Chuot and otherPiece.type == Voi: # Chuot > Voi
                captureScore = pieceScore.get(otherPiece.type)
                break
            elif pieceScore.get(pieceType) >= pieceScore.get(otherPiece.type):
                captureScore = pieceScore.get(otherPiece.type)
                break
            else:
                break
    return captureScore
    

# Evaluate a state
def evalute(state, side):
    blackScore = 0
    redScore = 0
    for piece in state.list_black:
        pieceType = piece.type
        if piece.position in trapPosition:
            blackScore += 0
        elif piece.position in waterPosition:
            blackScore += pieceScore.get(pieceType) / 2
        else:
            blackScore += pieceScore.get(pieceType)
    for piece in state.list_red:
        pieceType = piece.type
        if piece.position in trapPosition:
            redScore += 0
        elif piece.position in waterPosition:
            redScore += pieceScore.get(pieceType) / 2
        else:
            redScore += pieceScore.get(pieceType)

    if side == "black":
        return blackScore - redScore / 2
    else:
        return redScore - blackScore / 2

# do the move
def doMove(move, board):
    # blackList = board.list_black
    # redList = board.list_red
    blackList = []
    redList = []

    for piece in board.list_black:
        blackList.append(Piece(piece.type, piece.position))
    for piece in board.list_red:
        redList.append(Piece(piece.type, piece.position))

    piece, nextPos = move

    # Find piece in board
    thePiece = None
    for x in blackList:
        if x.type == piece.type and x.position == piece.position:
            thePiece = x

    if thePiece is None:
        for x in redList:
            if x.type == piece.type and x.position == piece.position:
                thePiece = x

    # Check if any piece at next pos
    theOtherPiece = None
    for x in blackList:
        if x.position == nextPos:
            theOtherPiece = x
            blackList.remove(theOtherPiece);

    if theOtherPiece is None:
        for x in redList:
            if x.position == nextPos:
                theOtherPiece = x
                redList.remove(theOtherPiece)

    # Move the Piece to next Pos
    thePiece.position = nextPos

    newState = Board(blackList, redList)

    return newState
    


# check in range
def inRange(pos):
    y = pos[0]
    x = pos[1]
    if x < 1 or x > 7 or y < 1 or y > 9:
        return False
    else:
        return True

# Check if win
def isGoal(state, side):
    if side == "black":
        for piece in state.list_black:
            if piece.position == blackWinPosition:
                # Game over, black won
                pass
    if side == "red":
        for piece in state.list_red:
            if piece.position == redWinPosition:
                # Game over, red won
                pass