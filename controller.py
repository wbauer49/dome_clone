
import pygame
import time

import constants
from constants import *
import env


class Controller:

    drag_piece = None
    drag_pos = None
    start_coords = None
    last_step_time = 0
    space_pressed_time = 0

    def check_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                env.grid.step_forward()
                self.space_pressed_time = time.time()
                self.last_step_time = time.time()
            elif event.key == pygame.K_r:
                env.grid.reset_level()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                clicked_piece = env.hand.get_clicked_piece(event.pos[0], event.pos[1])
                if clicked_piece:
                    self.drag_piece = clicked_piece

                if self.drag_piece:
                    self.drag_pos = (event.pos[0] - PIX // 2, event.pos[1] - PIX // 2)
                    if env.grid.play_clicked_piece(event.pos[0], event.pos[1], self.drag_piece):
                        self.drag_piece = None

            elif event.button == 3:  # right click
                if self.drag_piece:
                    self.drag_piece.rotate()

        elif event.type == pygame.MOUSEMOTION:
            if self.drag_piece:
                self.drag_pos = (event.pos[0] - PIX // 2, event.pos[1] - PIX // 2)

    def check_pressed_keys(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_SPACE]:
            if time.time() - self.last_step_time >= constants.STEP_TIME:
                env.grid.step_forward()
                self.last_step_time = time.time()
