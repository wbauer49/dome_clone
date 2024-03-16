
import pieces


class Player:

    def __init__(self, player_num):
        self.player_num = player_num

        self.hand = self.draw_hand()

    def draw_hand(self):  # TODO
        return [
            pieces.Piece(),
            pieces.Piece({
                (0, 0): pieces.Block(inputs=[], outputs=[]),
                (0, 1): pieces.Block(inputs=[], outputs=[]),
            }),
            pieces.Piece({
                (0, 0): pieces.Block(inputs=[pieces.L], outputs=[]),
                (1, 0): pieces.Block(inputs=[], outputs=[pieces.R]),
            }),
            pieces.Piece({
                 (0, 0): pieces.Block(inputs=[pieces.R, pieces.U, pieces.L, pieces.D], outputs=[]),
            }),
        ]
