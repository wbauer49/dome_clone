
import copy

import env


class Item:
    b_cost = 0
    g_cost = 0

    def unique_function(self, card):
        pass


class DuplicateCard(Item):

    text = "Duplicate a card in hand"
    b_cost = 4

    def unique_function(self, card):
        env.players.get_curr_deck().append(copy.deepcopy(card))


class TrashCard(Item):

    text = "Trash a card in hand"
    b_cost = 3

    def unique_function(self, card):
        env.players.get_curr_deck().remove(card)
        env.hand.cards.remove(card)


class IncreaseDrawsCard(Item):

    text = "Add +1 Draw to a card in hand"
    b_cost = 2

    def unique_function(self, card):
        card.draw_cards += 1


class AddBlockToPiece(Item):
    text = "Add block to piece in hand"
    g_cost = 3

    def unique_function(self, card):
        card.piece.add_block()


class AddInputToPiece(Item):
    text = "Add input to piece in hand"
    g_cost = 1

    def unique_function(self, card):
        card.piece.add_input()


class AddOutputToPiece(Item):
    text = "Add output to piece in hand"
    b_cost = 1
    g_cost = 3

    def unique_function(self, card):
        card.piece.add_output()


STARTING_ITEMS = [
    DuplicateCard(),
    TrashCard(),
    IncreaseDrawsCard(),
    AddBlockToPiece(),
    AddInputToPiece(),
    AddOutputToPiece(),
]
