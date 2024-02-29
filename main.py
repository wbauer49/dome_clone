
import pygame
import time

import constants
import controller
import grid
import rendering
import env


try:
    env.controller = controller.Controller()
    env.renderer = rendering.Renderer()
    env.grid = grid.Grid()

    running = True
    while running:
        start_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
            env.controller.check_event(event)
        env.controller.check_pressed_keys()

        env.renderer.render()

        sleep_time = (time.time() - start_time) / constants.FRAME_RATE
        if sleep_time > 0:
            time.sleep(sleep_time)
        else:
            print("frame lag")


except KeyboardInterrupt:
    print("exited")
finally:
    pygame.quit()
