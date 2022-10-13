import abc
from app.domain.fem import FEM


class RepoInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load(self, model: FEM, file: str) -> FEM:
        raise NotImplementedError

    @abc.abstractmethod
    def write(self, model: FEM, file: str) -> None:
        raise NotImplementedError
