from Game.AI.AlphaBetaAi import AlphaBetaAi
from Game.Board import GameBoard
from tensorflow.keras import layers, models, optimizers


class ReinforcementAI(AlphaBetaAi):
    def __init__(self, compiled_model: models.Model = None, learning_rate: float = 0.001) -> None:
        """A Reinforcement learning AI"""
        super().__init__(depth=1)

        if compiled_model is None:
            model = models.Sequential(
                layers=[
                    layers.Dense(
                        64,
                        activation='relu',
                        input_shape=(8, 8)
                    ),
                    layers.Dense(64, activation='relu'),
                    layers.Dense(1, activation='sigmoid'),
                ]
            )

            model.compile(
                optimizer=optimizers.Adam(learning_rate=learning_rate),
                loss='binary_crossentropy'
            )
            compiled_model = model

        self.model = compiled_model

    def base_prune(self, board: GameBoard) -> int:
        """Pruning the base case based on the NN"""
        result = self.model.predict(board.board.reshape(1, 8, 8))[0][0]
        print(result)
        return result
