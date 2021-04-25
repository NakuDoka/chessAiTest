import os
import pygame
import chess
import random
import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers

WIDTH = 640
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Chess")
board = chess.Board()
FPS = 20
pygame.init()
Pause = False
pieces = []
helplines = []
turn = 0

#Images
bg = pygame.image.load('images/background.jpg')
bg = pygame.transform.scale(bg, (640, 640))
bishopB = pygame.image.load('images/bishopB.png')
bishopW = pygame.image.load('images/bishopW.png')
kingB = pygame.image.load('images/kingB.png')
kingW = pygame.image.load('images/kingW.png')
knightB = pygame.image.load('images/knightB.png')
knightW = pygame.image.load('images/knightW.png')
pawnB = pygame.image.load('images/pawnB.png')
pawnW = pygame.image.load('images/pawnW.png')
queenB = pygame.image.load('images/queenB.png')
queenW = pygame.image.load('images/queenW.png')
rookB = pygame.image.load('images/rookB.png')
rookW = pygame.image.load('images/rookW.png')

# ImageMap
ImageMap = {'p': pawnB, 'P': pawnW, 'r': rookB, 'R': rookW, 'n': knightB, 'N': knightW, 'b': bishopB, 'B': bishopW, 'q': queenB, 'Q': queenW, 'k': kingB, 'K': kingW}

# Lines
s = pygame.Surface((80, 80))
s.set_alpha(200)
s.fill((221,40,40))

class Piece(object):
    def __init__(self, x, y, row, col, name, image):
        self.x = x
        self.y = y
        self.row = row
        self.col = col
        self.name = name
        self.image = image

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def updateXY(self):
        self.y = self.col * 80 - 82
        self.x = self.row * 80 -82

class Helpline(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self, win):
        WIN.blit(s, (self.x, self.y))
        #pygame.draw.rect(WIN, (221,40,40, 0), rect=((self.x, self.y), (80, 80)))

def redrawGameWindow():
    WIN.blit(bg, (0,0))
    for helpline in helplines:
        helpline.draw(WIN)
    for piece in pieces:
        piece.draw(WIN)
    
    pygame.display.update()

def getPieces(board):
    for i in range(64):
        if board.piece_at(i) is not None:
            row = 7 - (i // 8) + 1
            col = (i % 8) + 1
            x = (col * 80 - 82)
            y = (row * 80 - 82)
            piece =  board.piece_at(i).symbol()
            image = ImageMap[piece]
            image = pygame.transform.scale(image, (80, 80)) 
            pieces.append(Piece(x,y,col, row, piece, image))

def checkLoss():
    global board
    if board.is_game_over():
        board.result()

def movePice(mousePosition):
    res = whatPositionIsclicked(mousePosition)
    piecer = None
    if res:
        cols, rows = res
        for piece in pieces:
            if piece.col == cols and piece.row == rows:
                return piece
                
def whatPositionIsclicked(mousePosition):
    x, y = mousePosition
    numbers = [80, 160, 240, 320, 400, 480, 560, 640]
    col = 0
    row = 0
    for i in numbers:
        col +=1
        if y <= i:
            for j in numbers:
                row +=1
                if x <= j:
                    break
                else:
                    continue
            break
        else:
            row = 0
    return col, row

def checkMove(piece, row, col, promotion):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    oldPos = letters[piece.row - 1], str(9 - piece.col)
    newPos = letters[row - 1], str(9 - col)
    pos = (oldPos+newPos)
    poss = ''.join(pos)
    print(poss)
    if poss[:2] == poss[2:]:
        pass
    elif (piece.name == 'P' and poss[1] == '7' and poss[3] == '8') or (piece.name == 'p' and poss[1] == '2' and poss[3] == '1'):
        poss = poss + promotion
        poss = ''.join(poss)
        move = chess.Move.from_uci(poss)
        if move in board.legal_moves:
            board.push(move)
            pieces.clear()
            getPieces(board)
            return True
    else:
        move = chess.Move.from_uci(poss)
        if move in board.legal_moves:
            board.push(move)
            pieces.clear()
            getPieces(board)
            return True
        
def showCurrentMoves(piece):
    helplines.clear()
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    oldPos = letters[piece.row - 1], str(9 - piece.col)
    pos = ''.join(oldPos)
    for move in board.legal_moves:
        if str(move)[:2] == pos:
            tile = str(move)[2:]
            row = letters.index(tile[0]) 
            col = 8 - int(tile[1])
            x = row * 80
            y = col * 80
            helplines.append(Helpline(x, y))



def AinextMove():
    totalMoves = board.legal_moves.count()
    i = -1
    s = random.randint(0, totalMoves)
    for move in board.legal_moves:
        i +=1
        if i == s:
            board.push(move)
            pieces.clear()
            getPieces(board)
            return True




def main():
    global Pause
    run = True
    clock = pygame.time.Clock()
    piece_dragging = False
    current_row = None
    current_col = None
    active_piece = None
    last_piece = None
    turn = 0
    promo = 'q'
    getPieces(board)
    while run:
        clock.tick(FPS)
        # Ifall man förlorar
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

        # Checka events
        for event in pygame.event.get():
            # Avsluta
            if event.type == pygame.QUIT:
                run = False
            # Ifall man klickar 
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if Pause:
                    # changeFigure(pos, active_piece) # Sätter till senare det är då man byter figur på en pawn
                    print('pause')
                else:
                    piece_dragging = True
                    active_piece = movePice(pos)
                    if len(helplines) > 0 and last_piece:
                        poss = pygame.mouse.get_pos()
                        col, row = whatPositionIsclicked(poss)
                        canGo = checkMove(last_piece, row, col, promo)
                        if canGo:
                            helplines.clear()
                            if turn == 0:
                                turn = 1
                            else:
                                turn = 0
                    if active_piece:
                        showCurrentMoves(active_piece)
                        if active_piece.name.isupper() and turn == 0:
                            last_piece = active_piece
                        elif active_piece.name.islower() and turn == 1:
                            last_piece = active_piece
                        current_col = active_piece.col
                        current_row = active_piece.row
                    
            # Mus motion
            elif event.type == pygame.MOUSEMOTION:
                # Om man håller in musen
                if piece_dragging:
                    x, y = pygame.mouse.get_pos()
                    if active_piece:
                        if active_piece.name.isupper() and turn == 0:
                            active_piece.x = x - 40
                            active_piece.y = y - 40
                        elif active_piece.name.islower() and turn == 1:
                            active_piece.x = x - 40
                            active_piece.y = y - 40

            # Ifall man slutar hålla in
            elif event.type == pygame.MOUSEBUTTONUP:
                if not Pause:
                    poss = pygame.mouse.get_pos()
                    col, row = whatPositionIsclicked(poss)
                    if active_piece:
                        if active_piece.col == col and active_piece.row == row: # ser ifall man inte flyttat på pjäsen
                            pass
                        else:
                            canGo = checkMove(active_piece, row, col, promo)
                            if canGo:
                                helplines.clear()
                                if turn == 0:
                                    turn = 1
                                else:
                                    turn = 0
                            else:
                                active_piece.col = current_col
                                active_piece.row = current_row

                    if current_row and current_col and active_piece:
                        active_piece.col = current_col
                        active_piece.row = current_row
                        active_piece.updateXY()
                    piece_dragging = False

            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    if (event.unicode == 'q' or event.unicode == 'n' or event.unicode ==  'b' or event.unicode ==  'r'):
                        promo = event.unicode

            redrawGameWindow()

    pygame.quit()

main()