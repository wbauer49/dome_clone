
import pygame

from constants import *
import env


class Renderer:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(COLORS.BACKGROUND)
        pygame.display.flip()

    def render(self):
        self.screen.fill(COLORS.BACKGROUND)

        self.screen.blit(env.grid.surface, env.grid.location)
        self.screen.blit(env.hand.surface, env.hand.location)

        if env.controller.drag_piece is not None:
            self.screen.blit(env.controller.drag_piece.surface, env.controller.drag_pos)

        pygame.display.flip()
