
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
        for i in range(1, self.size):
            pygame.draw.line(self.surface, COLORS.GRID_LINE, (i * PIX, 0), (i * PIX, self.size * PIX))
            pygame.draw.line(self.surface, COLORS.GRID_LINE, (0, i * PIX), (self.size * PIX, i * PIX))

    def play_clicked_piece(self, x, y, drag_piece):
        col = (x - self.location[0]) // PIX
        row = (y - self.location[1]) // PIX

        connected = False
        for (b_x, b_y), block in drag_piece.blocks.items():
            if not (0 <= col + b_x < self.size and 0 <= row + b_y < self.size) or self.matrix[col + b_x][row + b_y]:
                return False
            print("a")

            for in_dir in block.inputs:
                if (
                        (
                                in_dir == R and col + b_x + 1 < self.size and self.matrix[col + b_x + 1][row + b_y]
                                and L in self.matrix[col + b_x + 1][row + b_y].outputs
                        ) or (
                                in_dir == U and row + b_y - 1 >= 0 and self.matrix[col + b_x][row + b_y - 1]
                                and D in self.matrix[col + b_x][row + b_y - 1].outputs
                        ) or (
                                in_dir == L# and col + b_x - 1 >= 0 and self.matrix[col + b_x - 1][row + b_y]
                                #and R in self.matrix[col + b_x - 1][row + b_y].outputs
                        ) or (
                                in_dir == D and row + b_y + 1 < self.size and self.matrix[col + b_x][row + b_y + 1]
                                and U in self.matrix[col + b_x][row + b_y + 1].outputs
                        )
                ):
                    connected = True
                    print("b")

        print("c")
        if connected:
            for (b_x, b_y), block in drag_piece.blocks.items():
                self.matrix[col + b_x][row + b_y] = block

            self.surface.blit(drag_piece.surface, (col * PIX, row * PIX))
            return True

        return False


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

    def render(self):
        self.surface = pygame.surface.Surface((self.card_width * 4, self.card_height * 2))
        for i, piece in enumerate(self.cards):
            x = self.card_width * (i % 4) + self.card_margin
            y = self.card_height * (i // 4) + self.card_margin
            pygame.draw.rect(self.surface, COLORS.CARD,
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

        self.render()

    def draw_card(self):
        self.cards.append(self.deck.pop())

    def get_clicked_piece(self, x, y):
        x -= self.location[0]
        y -= self.location[1]
        if (
                0 < x < self.card_width * 4 and 0 < y < self.card_height * 2 and
                self.card_margin < x % self.card_width < self.card_width - self.card_margin and
                self.card_margin < y % self.card_height < self.card_height - self.card_margin
        ):
            i = 4 * (y // self.card_height) + x // self.card_width
            if i < len(self.cards):
                return self.cards[i]
        return None
