
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

    def unique_function(self):
        pass
