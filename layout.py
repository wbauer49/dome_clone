import copy

import items
import pygame
import random

import env
from constants import *
import pieces


class Bonus:

    def __init__(self, bonus_def):
        self.currency, self.operation, value_str = list(bonus_def)
        self.value = int(value_str)

    def render(self):
        surface = pygame.surface.Surface((PIX, PIX))

        if self.currency == "b":
            color = (20, 50, 100),
        else:
            color = (20, 100, 50)
        pygame.draw.rect(surface, color, (0, 0, PIX, PIX))

        font = pygame.font.SysFont(pygame.font.get_default_font(), 60)
        text_surface = font.render(f"{self.operation}{self.value}", False, COLORS.BACKGROUND)
        surface.blit(text_surface, ((PIX - text_surface.get_width()) // 2, (PIX - text_surface.get_height()) // 2))

        return surface

    def add_money(self):
        if self.currency == "b":
            if self.operation == "+":
                env.counter.b_money += self.value
            else:
                env.counter.b_money *= self.value
        else:
            if self.operation == "+":
                env.counter.g_money += self.value
            else:
                env.counter.g_money *= self.value

        env.counter.render()


class Grid:

    location = (0, 0)
    size = 13

    matrix = None
    bonuses = None
    surface = None

    BONUS_LOCATIONS = {
        "b+1": [(4, 0), (2, 2)],
        "b+2": [(4, 2)],
        "b*2": [(6, 1), (5, 3)],
        "b*3": [(6, 6)],
        "g+1": [(1, 1), (4, 4), (7, 3)],
        "g*2": [(5, 5)],
    }

    def __init__(self):
        self.construct_bonuses()
        self.reset_grid()

    def construct_bonuses(self):
        self.bonuses = {}
        for bonus_def, locations in self.BONUS_LOCATIONS.items():
            for (a, b) in locations:
                for (a_offset, b_offset) in [(a, b), (-a, b), (-a, -b), (a, -b), (b, a), (-b, a), (-b, -a), (b, -a)]:
                    self.bonuses[(self.size // 2 + a_offset), self.size // 2 + b_offset] = Bonus(bonus_def)

    def reset_grid(self):
        self.surface = pygame.surface.Surface((self.size * PIX, self.size * PIX))
        self.matrix = []
        for row in range(self.size + 1):
            self.matrix.append([])
            for col in range(self.size + 1):
                self.matrix[row].append(None)

        starter_piece = pieces.StarterPiece()
        mid = self.size // 2
        self.matrix[mid][mid] = starter_piece
        for (b_x, b_y), block in starter_piece.blocks.items():
            self.matrix[mid + b_x][mid + b_y] = block
        self.surface.blit(starter_piece.surface, (mid * PIX, mid * PIX))

        self.render()

    def render(self):
        for (a, b), bonus in self.bonuses.items():
            bonus_surface = bonus.render()
            self.surface.blit(bonus_surface, (a * PIX, b * PIX))

        for i in range(1, self.size):
            pygame.draw.line(self.surface, COLORS.GRID_LINE, (i * PIX, 0), (i * PIX, self.size * PIX))
            pygame.draw.line(self.surface, COLORS.GRID_LINE, (0, i * PIX), (self.size * PIX, i * PIX))

    def play_clicked_piece(self, event, drag_piece):

        x = (event.pos[0] - self.location[0]) // PIX
        y = (event.pos[1] - self.location[1]) // PIX

        connected = False
        for (b_x, b_y), block in drag_piece.blocks.items():
            if not (0 <= x + b_x < self.size and 0 <= y + b_y < self.size) or self.matrix[x + b_x][y + b_y]:
                return False

            for in_dir in block.inputs:
                if (
                        (
                                in_dir == R and x + b_x + 1 < self.size and self.matrix[x + b_x + 1][y + b_y]
                                and L in self.matrix[x + b_x + 1][y + b_y].outputs
                        ) or (
                                in_dir == U and y + b_y - 1 >= 0 and self.matrix[x + b_x][y + b_y - 1]
                                and D in self.matrix[x + b_x][y + b_y - 1].outputs
                        ) or (
                                in_dir == L and x + b_x - 1 >= 0 and self.matrix[x + b_x - 1][y + b_y]
                                and R in self.matrix[x + b_x - 1][y + b_y].outputs
                        ) or (
                                in_dir == D and y + b_y + 1 < self.size and self.matrix[x + b_x][y + b_y + 1]
                                and U in self.matrix[x + b_x][y + b_y + 1].outputs
                        )
                ):
                    connected = True

        if connected:
            for (b_x, b_y), block in drag_piece.blocks.items():
                self.matrix[x + b_x][y + b_y] = copy.deepcopy(block)

                bonus = self.bonuses.get((x + b_x, y + b_y), None)
                if bonus:
                    bonus.add_money()  # TODO: make multiplication bonuses happen before addition

            self.surface.blit(drag_piece.surface, ((x + drag_piece.min_x) * PIX, (y + drag_piece.min_y) * PIX))
            return True

        return False


class Card:

    def __init__(self, piece, draw_cards=0):
        self.piece = piece
        self.draw_cards = draw_cards

    def unique_function(self):
        pass

    def use_abilities(self):
        for i in range(self.draw_cards):
            env.hand.draw_card()


class Hand:

    card_width = 220
    card_height = 330
    card_margin = 15
    text_margin = 20
    num_cols = 4
    num_rows = 2
    location = (WIDTH - card_width * num_cols, 0)

    hand_size = 4

    surface = None
    deck = None
    cards = None
    selected_card = None

    def __init__(self):
        self.start_turn()

    def render(self):
        self.surface = pygame.surface.Surface((self.card_width * self.num_cols, self.card_height * self.num_rows))
        for i, card in enumerate(self.cards):
            x = self.card_width * (i % self.num_cols) + self.card_margin
            y = self.card_height * (i // self.num_cols) + self.card_margin
            pygame.draw.rect(self.surface, COLORS.CARD,
                             (x, y, self.card_width - 2 * self.card_margin, self.card_height - 2 * self.card_margin))

            if card.draw_cards > 0:
                font = pygame.font.SysFont(pygame.font.get_default_font(), 30)
                text_surface = font.render(f"Draw {card.draw_cards}", False, COLORS.CARD_TEXT)
                self.surface.blit(text_surface, (x + self.text_margin, y + self.text_margin))

            piece = card.piece
            scale = 1.4 / piece.scale ** 0.5
            scaled_piece = pygame.transform.scale_by(piece.surface, scale)
            piece_margin = (self.card_width - 2 * self.card_margin - piece.scale * scale * PIX) // 2
            self.surface.blit(scaled_piece,
                              (x + piece_margin, y + self.card_height - 2 * self.card_margin - piece.scale * scale * PIX - piece_margin))

    def start_turn(self):
        self.deck = env.players.get_curr_deck().copy()
        random.shuffle(self.deck)

        self.cards = []
        for i in range(self.hand_size):
            self.draw_card()

        self.render()

    def draw_card(self):
        if len(self.deck) > 0 and len(self.cards) < 8:
            self.cards.append(self.deck.pop())

    def get_clicked_card(self, event):
        x = event.pos[0] - self.location[0]
        y = event.pos[1] - self.location[1]
        if (
                0 < x < self.card_width * 4 and 0 < y < self.card_height * 2 and
                self.card_margin < x % self.card_width < self.card_width - self.card_margin and
                self.card_margin < y % self.card_height < self.card_height - self.card_margin
        ):
            i = 4 * (y // self.card_height) + x // self.card_width
            if i < len(self.cards):
                self.selected_card = i
                return self.cards[i]
        return None

    def play_selected_card(self):
        card = self.cards.pop(self.selected_card)
        card.use_abilities()

        self.selected_card = None
        self.render()


class Store:

    item_width = 450
    item_height = 60
    item_margin = 10
    text_margin = 10
    cost_width = 30
    num_cols = 2
    num_rows = 5
    location = (WIDTH - item_width * num_cols, HEIGHT - item_height * num_rows)
    surface = None

    def __init__(self):
        self.render()

        self.highlight_surface = pygame.surface.Surface((self.item_width, self.item_height)).convert_alpha()
        self.highlight_surface.fill((250, 250, 100, 50))

    def render(self):
        self.surface = pygame.surface.Surface((self.item_width * self.num_cols, self.item_height * self.num_rows))
        font = pygame.font.SysFont(pygame.font.get_default_font(), 30)

        for i, item in enumerate(items.STARTING_ITEMS):
            x = self.item_width * (i % self.num_cols) + self.item_margin
            y = self.item_height * (i // self.num_cols) + self.item_margin
            pygame.draw.rect(self.surface, COLORS.CARD,
                             (x, y, self.item_width - 2 * self.item_margin, self.item_height - 2 * self.item_margin))

            self.surface.blit(font.render(item.text, False, COLORS.CARD_TEXT), (x + self.text_margin, y + self.text_margin))
            self.surface.blit(font.render(str(item.b_cost), False, COLORS.BLUE_COST),
                              (x + self.item_width - 2 * self.item_margin - 2 * self.cost_width, y + self.text_margin))
            self.surface.blit(font.render(str(item.g_cost), False, COLORS.GREEN_COST),
                              (x + self.item_width - 2 * self.item_margin - self.cost_width, y + self.text_margin))

    def get_clicked_item(self, event):
        click_x = event.pos[0] - self.location[0]
        click_y = event.pos[1] - self.location[1]
        if (
                0 < click_x < self.item_width * self.num_cols and 0 < click_y < self.item_height * self.num_rows and
                self.item_margin < click_x % self.item_width < self.item_width - self.item_margin and
                self.item_margin < click_y % self.item_height < self.item_height - self.item_margin
        ):
            x = click_x // self.item_width
            y = click_y // self.item_height
            i = y * self.num_cols + x
            if i < len(items.STARTING_ITEMS):
                return items.STARTING_ITEMS[i]

        return None

    def highlight_item(self, item):
        i = items.STARTING_ITEMS.index(item)
        x = i % self.num_cols
        y = i // self.num_cols

        self.render()
        self.surface.blit(self.highlight_surface, (x * self.item_width, y * self.item_height))


class Counter:

    width = 280
    height = 50
    text_margin = 10
    cost_width = 65
    location = (Hand.location[0], Hand.card_height * Hand.num_rows)
    surface = None

    b_money = None
    g_money = None
    buys = None

    def __init__(self):
        self.reset_money()
        self.render()

    def render(self):
        self.surface = pygame.surface.Surface((self.width, self.height))
        font = pygame.font.SysFont(pygame.font.get_default_font(), 45)

        self.surface.blit(font.render(str(self.b_money), False, COLORS.BLUE_COST), (self.text_margin, self.text_margin))
        self.surface.blit(font.render(str(self.g_money), False, COLORS.GREEN_COST), (self.text_margin + self.cost_width, self.text_margin))
        self.surface.blit(font.render(f"{self.buys} Buys", False, COLORS.BUYS), (self.text_margin + self.cost_width * 2, self.text_margin))

    def reset_money(self):
        self.b_money = 0
        self.g_money = 0
        self.buys = 2
        self.render()

    def can_afford_item(self, item):
        return self.buys > 0 and self.b_money >= item.b_cost and self.g_money >= item.g_cost

    def pay_for_item(self, item):
        self.b_money -= item.b_cost
        self.g_money -= item.g_cost
        self.buys -= 1
        self.render()

        if self.buys == 0:
            env.players.next_turn()
