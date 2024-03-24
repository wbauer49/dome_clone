
import pygame
import time

import constants
from constants import *
import env


class Controller:

    drag_block = None
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
                self.start_coords = (event.pos[0] // PIX, event.pos[1] // PIX)
                if env.grid.coords_in_range(self.start_coords):
                    block = env.grid.get_grid_block(self.start_coords)
                    if block is not None and not block.is_wall:
                        self.drag_block = block
                        self.drag_pos = (event.pos[0] - PIX // 2, event.pos[1] - PIX // 2)

            else:  # right click
                if self.drag_block is not None:
                    self.drag_block.rotate()
                else:
                    coords = (event.pos[0] // PIX, event.pos[1] // PIX)
                    if env.grid.coords_in_range(coords):
                        block = env.grid.get_grid_block(coords)
                        block.rotate()

        elif event.type == pygame.MOUSEMOTION:
            if self.drag_block is not None:
                self.drag_pos = (event.pos[0] - PIX // 2, event.pos[1] - PIX // 2)

        elif event.type == pygame.MOUSEBUTTONUP:  # snap back to grid
            if self.drag_block is not None:
                if event.button == 1:
                    end_coords = (event.pos[0] // PIX, event.pos[1] // PIX)
                    if env.grid.coords_in_workspace(end_coords):
                        end_block = env.grid.get_grid_block(end_coords)
                        if end_block is None:  # if empty, drop the block here
                            env.grid.set_grid_block(end_coords, self.drag_block)
                            env.grid.set_grid_block(self.start_coords, None)

                self.drag_block = None

    def check_pressed_keys(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_SPACE]:
            if time.time() - self.last_step_time >= constants.STEP_TIME:
                env.grid.step_forward()
                self.last_step_time = time.time()
