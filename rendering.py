
import pygame

from constants import *
import env


class Renderer:

    layout_render = None

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.flip()

    def render(self):
        for row, row_list in enumerate(env.grid.grid):
            for col, block in enumerate(row_list):
                if block is None or block.is_wall:
                    continue
                self.screen.blit(block.sprite, (col * PIX, row * PIX))

        for i, piece in enumerate(env.players[0].hand):
            pygame.draw.rect(self.screen, (30, 30, 30), (170 * i + 50, HEIGHT - 250, 140, 230))

            scale = 1 / piece.scale ** 0.5
            scaled_piece = pygame.transform.scale_by(piece.surface, scale)
            margin = (120 - scale * piece.scale * PIX) // 2
            self.screen.blit(scaled_piece, (170 * i + 60 + margin, HEIGHT - 150 + margin))

        if env.controller.drag_block is not None:
            self.screen.blit(env.controller.drag_block.sprite, env.controller.drag_pos)

        pygame.display.flip()
