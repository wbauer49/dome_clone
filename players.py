
from constants import *
import layout
import pieces


STARTING_DECK = [
    layout.Card(
        pieces.Piece({
            (0, 0): pieces.Block(inputs=[L], outputs=[R])
        }),
        draw_cards=1
    ),
    layout.Card(
        pieces.Piece({
            (0, 0): pieces.Block(inputs=[L], outputs=[R, U]),
            (0, 1): pieces.Block(inputs=[], outputs=[R, L, D]),
        }),
        draw_cards=1
    ),
    layout.Card(
        pieces.Piece({
            (0, 0): pieces.Block(inputs=[L], outputs=[]),
            (1, 0): pieces.Block(inputs=[], outputs=[R]),
        }),
    ),
    layout.Card(
        pieces.Piece({
             (0, 0): pieces.Block(inputs=[R, U, L, D], outputs=[]),
        }),
        draw_cards=2
    )
] * 4


class Player:

    def __init__(self, player_num):
        self.player_num = player_num
        self.deck = STARTING_DECK.copy()
