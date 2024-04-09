
import pygame

from constants import *
import env


class Renderer:

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # , pygame.RESIZABLE)
        self.screen.fill(COLORS.BACKGROUND)
        pygame.display.flip()

    def render(self):
        self.screen.fill(COLORS.BACKGROUND)

        self.screen.blit(env.grid.surface, env.grid.location)
        self.screen.blit(env.hand.surface, env.hand.location)
        self.screen.blit(env.store.surface, env.store.location)
        self.screen.blit(env.money_counter.surface, env.money_counter.location)

        if env.controller.drag_piece is not None:
            self.screen.blit(env.controller.drag_piece.surface, env.controller.drag_pos)

        pygame.display.flip()
