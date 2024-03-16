
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
            pygame.draw.rect(self.screen, (30, 30, 30), (150 * i + 50, HEIGHT - 200, 120, 180))
            scale = piece.get_scale()
            for (x, y), block in piece.blocks.items():
                pygame.draw.rect(self.screen, (230, 230, 30), (150 * i + 70 + x * 100 // scale, HEIGHT - 130 + y * 100 // scale, 80 // scale, 80 // scale))

        if env.controller.drag_block is not None:
            self.screen.blit(env.controller.drag_block.sprite, env.controller.drag_pos)

        pygame.display.flip()
