import abc
from app.domain.fem import FEM


class Loader(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load(self, file) -> FEM:
        raise NotImplementedError
