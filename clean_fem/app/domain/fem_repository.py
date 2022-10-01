import abc
from typing import List

from app.domain.fem import FEM, Element, Node


class FEMRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add(self, model: FEM) -> FEM:
        raise NotImplementedError

    @abc.abstractmethod
    def all_elements(self) -> List[Element]:
        raise NotImplementedError

    @abc.abstractmethod
    def all_nodes(self) -> List[Node]:
        raise NotImplementedError

    @abc.abstractmethod
    def nb_elements(self) -> int:
        raise NotImplementedError