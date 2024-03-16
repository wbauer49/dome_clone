
R = 0
U = 1
L = 2
D = 3


class Block:

    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs


class Piece:

    col = None
    row = None

    actions = 1
    blocks = {
        (0, 0): Block(inputs=[L], outputs=[R])
    }

    def __init__(self, blocks=None):
        if blocks is not None:
            self.blocks = blocks

    def unique_function(self):
        pass

    def get_scale(self):
        min_x = 0
        max_x = 0
        min_y = 0
        max_y = 0
        for coord in self.blocks:
            if coord[0] < min_x:
                min_x = coord[0]
            if coord[0] > max_x:
                max_x = coord[0]
            if coord[1] < min_y:
                min_y = coord[1]
            if coord[1] > max_y:
                max_y = coord[1]

        return max(max_x - min_x, max_y - min_y) + 1
