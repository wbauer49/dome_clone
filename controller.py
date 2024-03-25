
import pygame
import time

import constants
from constants import *
import env


class Controller:

    drag_piece = None
    drag_pos = None
    start_coords = None
    space_pressed_time = 0

    def set_drag_pos(self, event):
        if self.drag_piece:
            self.drag_pos = (event.pos[0] + self.drag_piece.min_x * PIX - PIX // 2,
                             event.pos[1] + self.drag_piece.min_y * PIX - PIX // 2)

    def check_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                env.grid.reset_grid()
                env.hand.start_turn(env.players[0])

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                clicked_piece = env.hand.get_clicked_piece(event.pos[0], event.pos[1])
                if clicked_piece:
                    self.drag_piece = clicked_piece
                    if self.drag_piece:
                        self.set_drag_pos(event)

                if env.grid.play_clicked_piece(event.pos[0], event.pos[1], self.drag_piece):
                    self.drag_piece = None

            elif event.button == 3:  # right click
                if self.drag_piece:
                    self.drag_piece.rotate()
                    self.set_drag_pos(event)

        elif event.type == pygame.MOUSEMOTION:
            if self.drag_piece:
                self.set_drag_pos(event)
