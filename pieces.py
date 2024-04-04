
import copy
import pygame

from constants import *


MAIN_MARGIN = 8
CONNECTOR_MARGIN = 14
INPUT_PIX = 18


class Block:

    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs

    def rotate(self):
        for i, in_dir in enumerate(self.inputs):
            self.inputs[i] = (in_dir - 1) % 4
        for i, out_dir in enumerate(self.outputs):
            self.outputs[i] = (out_dir - 1) % 4


class Piece:

    col = None
    row = None
    min_x = None
    max_x = None
    min_y = None
    max_y = None
    scale = None
    surface = None

    blocks = {
        (0, 0): Block(inputs=[], outputs=[])
    }
    color = COLORS.PIECE

    def __init__(self, blocks=None):
        if blocks is not None:
            self.blocks = blocks

        self.render()

    def render(self):
        self.get_scale()
        self.surface = pygame.surface.Surface(((self.max_x - self.min_x + 1) * PIX, (self.max_y - self.min_y + 1) * PIX))
        self.surface.set_colorkey((0, 0, 0))

        for (x1, y1) in self.blocks:
            for (x2, y2) in self.blocks:
                rect_x = None
                rect_y = None
                if (x1 + 1, y1) == (x2, y2):
                    rect_x = x1 - self.min_x + 0.5
                    rect_y = y1 - self.min_y
                elif (x1, y1 + 1) == (x2, y2):
                    rect_x = x1 - self.min_x
                    rect_y = y1 - self.min_y + 0.5

                if rect_x is not None:
                    pygame.draw.rect(self.surface, COLORS.CONNECTOR,
                                     (rect_x * PIX + CONNECTOR_MARGIN, rect_y * PIX + CONNECTOR_MARGIN,
                                      PIX - 2 * CONNECTOR_MARGIN, PIX - 2 * CONNECTOR_MARGIN))

        for (x, y), block in self.blocks.items():
            pygame.draw.rect(self.surface, self.color,
                             ((x - self.min_x) * PIX + MAIN_MARGIN, (y - self.min_y) * PIX + MAIN_MARGIN,
                              PIX - 2 * MAIN_MARGIN, PIX - 2 * MAIN_MARGIN))

            for in_dir in block.inputs:
                if in_dir == R:
                    offset1 = (PIX - MAIN_MARGIN, MAIN_MARGIN)
                    offset2 = (PIX - MAIN_MARGIN, PIX // 2 + INPUT_PIX // 2)
                    shape = (MAIN_MARGIN, PIX // 2 - MAIN_MARGIN - INPUT_PIX // 2)
                elif in_dir == U:
                    offset1 = (MAIN_MARGIN, 0)
                    offset2 = (PIX // 2 + INPUT_PIX // 2, 0)
                    shape = (PIX // 2 - MAIN_MARGIN - INPUT_PIX // 2, MAIN_MARGIN)
                elif in_dir == L:
                    offset1 = (0, MAIN_MARGIN)
                    offset2 = (0, PIX // 2 + INPUT_PIX // 2)
                    shape = (MAIN_MARGIN, PIX // 2 - MAIN_MARGIN - INPUT_PIX // 2)
                elif in_dir == D:
                    offset1 = (MAIN_MARGIN, PIX - MAIN_MARGIN)
                    offset2 = (PIX // 2 + INPUT_PIX // 2, PIX - MAIN_MARGIN)
                    shape = (PIX // 2 - MAIN_MARGIN - INPUT_PIX // 2, MAIN_MARGIN)
                else:
                    raise Exception("illegal input direction")

                for offset in [offset1, offset2]:
                    pygame.draw.rect(self.surface, COLORS.INPUT,
                                     ((x - self.min_x) * PIX + offset[0], (y - self.min_y) * PIX + offset[1], shape[0], shape[1]))

            for out_dir in block.outputs:
                if out_dir == R:
                    offset = (PIX - MAIN_MARGIN, PIX // 2 - INPUT_PIX // 2)
                    shape = (MAIN_MARGIN, INPUT_PIX)
                elif out_dir == U:
                    offset = (PIX // 2 - INPUT_PIX // 2, 0)
                    shape = (INPUT_PIX, MAIN_MARGIN)
                elif out_dir == L:
                    offset = (0, PIX // 2 - INPUT_PIX // 2)
                    shape = (MAIN_MARGIN, INPUT_PIX)
                elif out_dir == D:
                    offset = (PIX // 2 - INPUT_PIX // 2, PIX - MAIN_MARGIN)
                    shape = (INPUT_PIX, MAIN_MARGIN)
                else:
                    raise Exception("illegal output direction")

                pygame.draw.rect(self.surface, COLORS.OUTPUT,
                                 ((x - self.min_x) * PIX + offset[0], (y - self.min_y) * PIX + offset[1], shape[0], shape[1]))

    def rotate(self):
        new_blocks = {}
        for (x, y), block in self.blocks.items():
            block.rotate()
            new_blocks[(-y, x)] = block

        self.blocks = new_blocks
        self.render()

    def get_scale(self):
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0
        for coords in self.blocks:
            if coords[0] < self.min_x:
                self.min_x = coords[0]
            if coords[0] > self.max_x:
                self.max_x = coords[0]
            if coords[1] < self.min_y:
                self.min_y = coords[1]
            if coords[1] > self.max_y:
                self.max_y = coords[1]

        self.scale = max(self.max_x - self.min_x, self.max_y - self.min_y) + 1

    def __deepcopy__(self, memo):
        self.surface = None

        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))

        self.render()
        result.render()
        return result


class StarterPiece(Piece):
    blocks = {
        (0, 0): Block(inputs=[], outputs=[R])
    }
    color = (100, 100, 100)
