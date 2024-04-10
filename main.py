
import pygame
import time

from constants import *
import controller
import layout
import rendering
import players
import env


try:
    env.players = players.Players(1)
    env.controller = controller.Controller()
    env.renderer = rendering.Renderer()
    env.grid = layout.Grid()
    env.hand = layout.Hand()
    env.store = layout.Store()
    env.counter = layout.Counter()

    running = True
    while running:
        start_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
            elif event.type == pygame.VIDEORESIZE:
                WIDTH = event.w
                HEIGHT = event.h
                env.renderer = rendering.Renderer()
                continue
            env.controller.check_event(event)

        env.renderer.render()

        sleep_time = (time.time() - start_time) / FRAME_RATE
        if sleep_time > 0:
            time.sleep(sleep_time)
        else:
            print("frame lag")


except KeyboardInterrupt:
    print("exited")
finally:
    pygame.quit()
