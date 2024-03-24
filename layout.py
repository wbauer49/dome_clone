
import pygame
import random

import env
from constants import *
import pieces


class Grid:

    size = 13
    location = (0, 0)

    matrix = None
    surface = None

    def __init__(self):
        self.reset_grid()

    def reset_grid(self):
        self.surface = pygame.surface.Surface((self.size * PIX, self.size * PIX))
        self.matrix = []
        for y in range(self.size + 1):
            self.matrix.append([])
            for x in range(self.size + 1):
                self.matrix[y].append(None)
        self.set_grid_block((0, 0), pieces.Starter())

        self.render()

    def render(self):
        for i in range(1, self.size):
            pygame.draw.line(self.surface, (255, 255, 255), (i * PIX, 0), (i * PIX, self.size * PIX))
            pygame.draw.line(self.surface, (255, 255, 255), (0, i * PIX), (self.size * PIX, i * PIX))

    def coords_in_range(self, coords):
        return 0 <= coords[0] < self.size and 0 <= coords[1] < self.size

    def get_grid_block(self, coords):
        return self.matrix[coords[1] + self.size // 2][coords[0] + self.size // 2]

    def set_grid_block(self, coords, block):
        self.matrix[coords[1] + self.size // 2][coords[0] + self.size // 2] = block


class Hand:
    card_width = 220
    card_height = 340
    card_margin = 15

    location = (WIDTH - card_width * 4, 0)
    hand_size = 4

    surface = None
    deck = None
    cards = None

    def __init__(self):
        self.start_turn(env.players[0])
        self.render()

    def render(self):
        self.surface = pygame.surface.Surface((self.card_width * 4, self.card_height * 3))
        for i, piece in enumerate(self.cards):
            x = self.card_width * (i % 4) + self.card_margin
            y = self.card_height * (i // 4) + self.card_margin
            pygame.draw.rect(self.surface, (30, 30, 30),
                             (x, y, self.card_width - 2 * self.card_margin, self.card_height - 2 * self.card_margin))

            scale = 1.4 / piece.scale ** 0.5
            scaled_piece = pygame.transform.scale_by(piece.surface, scale)
            piece_margin = (self.card_width - 2 * self.card_margin - piece.scale * scale * PIX) // 2
            self.surface.blit(scaled_piece,
                              (x + piece_margin, y + self.card_height - 2 * self.card_margin - piece.scale * scale * PIX - piece_margin))

    def start_turn(self, player):
        self.deck = player.deck.copy()
        random.shuffle(self.deck)

        self.cards = []
        for i in range(self.hand_size):
            self.draw_card()

    def draw_card(self):
        self.cards.append(self.deck.pop())
