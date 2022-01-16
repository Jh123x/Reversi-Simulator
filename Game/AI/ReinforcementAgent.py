from Game.AI.AlphaBetaAi import AlphaBetaAi
from Game.Board import GameBoard
from tensorflow.keras import models, optimizers


class ReinforcementAI(AlphaBetaAi):
    def __init__(self, model_path: str = None, model: models.Model = None, learning_rate: float = 0.001, loss: str = 'mse') -> None:
        """A Reinforcement learning AI
            Either must have model path and weights path
            Or a model (Not compiled)
        """
        if model is None and model_path is None:
            raise ValueError(
                "Must have model path and weights path or a model")

        super().__init__(depth=1)

        if model is None:
            model = models.load_model(model_path)

        model.compile(
            optimizer=optimizers.Adam(learning_rate=learning_rate),
            loss=loss
        )
        self.model = model

    def base_prune(self, board: GameBoard) -> int:
        """Pruning the base case based on the NN"""
        result = self.model.predict(board.board)[0][0]
        return result
