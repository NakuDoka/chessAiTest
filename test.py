import chess
from tensorflow import keras

board = chess.Board()

print(board.legal_moves.count())
for move in board.legal_moves:
    print(move)
    print(str(move)[:2])
