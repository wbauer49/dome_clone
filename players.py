
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


class Players:

    decks = []
    curr_player = 0

    def __init__(self, num_players):
        self.num_players = num_players
        for i in range(num_players):
            self.decks.append(STARTING_DECK.copy())

    def next_turn(self):
        self.curr_player = (self.curr_player + 1) % self.num_players

    def copy_current_deck(self):
        return self.decks[self.curr_player].copy()
