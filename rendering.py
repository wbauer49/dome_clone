
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

        if env.controller.drag_block is not None:
            self.screen.blit(env.controller.drag_block.sprite, env.controller.drag_pos)

        pygame.display.flip()
