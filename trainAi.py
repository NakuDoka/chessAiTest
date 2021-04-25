import chess
import random

board = chess.Board()

def AinextMove():
    totalMoves = board.legal_moves.count()
    i = -1
    s = random.randint(0, totalMoves)
    for move in board.legal_moves:
        i +=1
        if i == s:
            print(move)
            board.push(move)
            return True


def main():
    run = True
    turn = 0
    while run:
        if board.is_game_over():
            run = False
            print(board.result())

        if turn == 1:
            doneAiMove = AinextMove()
            if doneAiMove:
                turn = 0

        if turn == 0:
            doneAiMove = AinextMove()
            if doneAiMove:
                turn = 1

main()