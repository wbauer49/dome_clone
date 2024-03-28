import copy

import items
import pygame
import random

import env
from constants import *
import pieces


BONUS_LOCATIONS = {
    "b+1": [(4, 0), (2, 2)],
    "b+2": [(4, 2)],
    "b*2": [(6, 1), (5, 3)],
    "b*3": [(6, 6)],
    "g+1": [(1, 1), (4, 4), (7, 3)],
    "g*2": [(5, 5)],
}


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


class Grid:

    location = (0, 0)
    size = 13

    matrix = None
    bonuses = None
    surface = None

    def __init__(self):
        self.construct_bonuses()
        self.reset_grid()

    def construct_bonuses(self):
        self.bonuses = {}
        for bonus_def, locations in BONUS_LOCATIONS.items():
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
    card_height = 340
    card_margin = 15
    text_margin = 20
    location = (WIDTH - card_width * 4, 0)

    hand_size = 4

    surface = None
    deck = None
    cards = None
    selected_card = None

    def __init__(self):
        self.start_turn()

    def render(self):
        self.surface = pygame.surface.Surface((self.card_width * 4, self.card_height * 2))
        for i, card in enumerate(self.cards):
            x = self.card_width * (i % 4) + self.card_margin
            y = self.card_height * (i // 4) + self.card_margin
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
        self.deck = env.players.copy_current_deck()
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

    item_size = 120
    item_margin = 10
    location = (WIDTH - item_size * 6, HEIGHT - item_size * 3)
    surface = None

    def __init__(self):
        self.render()

    def render(self):
        self.surface = pygame.surface.Surface((self.item_size * 6, self.item_size * 3))
        for i, item in enumerate(items.STARTING_ITEMS):
            x = self.item_size * (i % 6) + self.item_margin
            y = self.item_size * (i // 6) + self.item_margin
            pygame.draw.rect(self.surface, COLORS.CARD,
                             (x, y, self.item_size - 2 * self.item_margin, self.item_size - 2 * self.item_margin))

    def get_clicked_item(self, event):
        x = event.pos[0] - self.location[0]
        y = event.pos[1] - self.location[1]
        if (
                0 < x < self.item_size * 6 and 0 < y < self.item_size * 3 and
                self.item_margin < x % self.item_size < self.item_size - self.item_margin and
                self.item_margin < y % self.item_size < self.item_size - self.item_margin
        ):
            i = 6 * (y // self.item_size) + x // self.item_size
            if i < len(items.STARTING_ITEMS):
                return items.STARTING_ITEMS[i]
        return None
