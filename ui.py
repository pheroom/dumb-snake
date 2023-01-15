import abc

from game import gSnake


class UI(abc.ABC):
    def __init__(self, game):
        self.game = game

    @abc.abstractmethod
    def run(self):
        pass