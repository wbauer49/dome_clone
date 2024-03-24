
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
        self.screen.blit(env.grid.surface, env.grid.location)
        self.screen.blit(env.hand.surface, env.hand.location)

        if env.controller.drag_block is not None:
            self.screen.blit(env.controller.drag_block.sprite, env.controller.drag_pos)

        pygame.display.flip()
