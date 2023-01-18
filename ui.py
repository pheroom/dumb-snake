import abc

from game import Snake


class UI(abc.ABC):
    def __init__(self, game):
        self.game = game

    @abc.abstractmethod
    def run(self):
        pass