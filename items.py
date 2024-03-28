import env


class Item:
    b_cost = 0
    g_cost = 0

    def unique_function(self):
        pass


class DuplicateFirstCard(Item):

    b_cost = 4

    def unique_function(self):
        card = env.hand.cards[0]
        env.players.curr_player.deck.append(card.copy())


class TrashFirstCard(Item):

    b_cost = 3

    def unique_function(self):
        card = env.hand.cards[0]
        env.players.curr_player.deck.remove(card)


class IncreaseDrawFirstCard(Item):

    b_cost = 2

    def unique_function(self):
        card = env.hand.cards[0]
        card.draw_cards += 1
        env.players.curr_player.deck.remove(card)


STARTING_ITEMS = [
    DuplicateFirstCard(),
    TrashFirstCard(),
    IncreaseDrawFirstCard(),
]
