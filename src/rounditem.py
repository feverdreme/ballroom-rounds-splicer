from abc import ABC, abstractmethod


class RoundItem(ABC):
    def __init__(self, index: int, artifacts_dir: str):
        if type(self) is RoundItem:
            raise TypeError("RoundItem is an abstract base class and cannot be instantiated directly.")
        
        self.index = index
        self.artifacts_dir = artifacts_dir

    @abstractmethod
    def generate_artifact(self):
        pass
