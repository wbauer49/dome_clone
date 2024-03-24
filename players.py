
from constants import *
import pieces


STARTING_DECK = [
    pieces.Piece({
        (0, 0): pieces.Block(inputs=[L], outputs=[R])
    }),
    pieces.Piece({
        (0, 0): pieces.Block(inputs=[], outputs=[]),
        (0, 1): pieces.Block(inputs=[], outputs=[]),
    }),
    pieces.Piece({
        (0, 0): pieces.Block(inputs=[L], outputs=[]),
        (1, 0): pieces.Block(inputs=[], outputs=[R]),
    }),
    pieces.Piece({
         (0, 0): pieces.Block(inputs=[R, U, L, D], outputs=[]),
    }),
]


class Player:

    def __init__(self, player_num):
        self.player_num = player_num
        self.deck = STARTING_DECK.copy()
