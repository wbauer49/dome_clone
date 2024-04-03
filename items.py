import env


class Item:
    b_cost = 0
    g_cost = 0

    def unique_function(self):
        pass


class DuplicateFirstCard(Item):

    text = "Duplicate first card in hand"
    b_cost = 4

    def unique_function(self):
        card = env.hand.cards[0]
        env.players.curr_player.deck.append(card.copy())


class TrashFirstCard(Item):

    text = "Trash first card in hand"
    b_cost = 3

    def unique_function(self):
        card = env.hand.cards[0]
        env.players.curr_player.deck.remove(card)


class IncreaseDrawFirstCard(Item):

    text = "Add +1 Draw to first card in hand"
    b_cost = 2

    def unique_function(self):
        card = env.hand.cards[0]
        card.draw_cards += 1
        env.players.curr_player.deck.remove(card)


class AddBlockToPiece(Item):
    text = "Add block to piece in hand"
    g_cost = 3


class AddInputToPiece(Item):
    text = "Add input to piece in hand"
    g_cost = 1


class AddOutputToPiece(Item):
    text = "Add output to piece in hand"
    b_cost = 1
    g_cost = 3


STARTING_ITEMS = [
    DuplicateFirstCard(),
    TrashFirstCard(),
    IncreaseDrawFirstCard(),
    AddBlockToPiece(),
    AddInputToPiece(),
    AddOutputToPiece(),
]
