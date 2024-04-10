
import copy

from constants import *
import env
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
            (0, 0): pieces.Block(inputs=[L], outputs=[U]),
            (0, 1): pieces.Block(inputs=[], outputs=[D]),
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
             (0, 0): pieces.Block(inputs=[L, U], outputs=[R, D]),
        }),
        draw_cards=2
    )
] * 2


class Players:

    decks = []
    curr_player = 0

    def __init__(self, num_players):
        self.num_players = num_players
        for i in range(num_players):
            self.decks.append(copy.deepcopy(STARTING_DECK))

    def next_turn(self):
        self.curr_player = (self.curr_player + 1) % self.num_players

        env.grid.reset_grid()
        env.hand.start_turn()
        env.counter.reset_money()

    def get_curr_deck(self):
        return self.decks[self.curr_player]
