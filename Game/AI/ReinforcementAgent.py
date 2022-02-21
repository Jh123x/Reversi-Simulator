from Game.AI.AlphaBetaAi import AlphaBetaAi
from Game.Board import GameBoard
from Game.PlayerEnum import PlayerTurn


class ReinforcementAI(AlphaBetaAi):
    def __init__(self, model_path: str = None, model: 'models.Model' = None, learning_rate: float = 0.001, loss: str = 'mse', depth:int=1) -> None:
        """A Reinforcement learning AI
            Either must have model path and weights path
            Or a model (Not compiled)
        """
        self.init = False
        self.learning_rate = learning_rate
        self.loss = loss
        self.model = model
        self.model_path = model_path
        self.base_player = PlayerTurn.WHITE if depth % 2 == 0 else PlayerTurn.BLACK
        super().__init__(depth)

    def base_prune(self, board: GameBoard) -> int:
        """Pruning the base case based on the NN"""
        if not self.init:
            from tensorflow.keras import models, optimizers
            if self.model is None and self.model_path is None:
                raise ValueError(
                    "Must have model path and weights path or a model")

            if self.model is None:
                model = models.load_model(self.model_path)
            else:
                model = self.model

            model.compile(
                optimizer=optimizers.Adam(learning_rate=self.learning_rate),
                loss=self.loss
            )
            self.model = model
            self.init = True
        reshaped = board.board.reshape((64, 1))
        result = self.model.predict(reshaped)[0][0]
        if board.current_turn == self.base_player:
            result = -result
        return result
