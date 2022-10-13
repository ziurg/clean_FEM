from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List, Optional, Literal, Union
from functools import singledispatchmethod

if TYPE_CHECKING:
    from app.domain.fem_repo_interface import RepoInterface


@dataclass
class Element:
    id: int
    nodes: List[int]

    def __contains__(self, nid: int) -> bool:
        return nid in self.nodes


@dataclass
class Node:
    id: int
    x: Optional[float] = 0.0
    y: Optional[float] = 0.0
    z: Optional[float] = 0.0


@dataclass
class FEM:
    nodes: Optional[Dict[int, Node]] = None
    elements: Optional[Dict[int, Element]] = None

    def __post_init__(self):
        self.nodes = {}
        self.elements = {}

    @singledispatchmethod
    def add(self, item: Union[Node, Element]) -> None:
        raise NotImplementedError("This object type can't be added to the model.")

    @add.register(Node)
    def _(self, n: Node) -> None:
        self.nodes[n.id] = n

    @add.register(Element)
    def _(self, e: Element) -> None:
        self.elements[e.id] = e

    @singledispatchmethod
    def __contains__(self, _) -> bool:
        raise NotImplementedError("This object type is not valid for this method.")

    @__contains__.register(Node)
    def _(self, n: Node) -> bool:
        return n.id in self.nodes

    @__contains__.register(Element)
    def _(self, e: Element) -> bool:
        return e.id in self.elements

    def load(self, fem_interface: "RepoInterface", file: str):
        return fem_interface.load(self, file)

    def write(self, fem_interface: "RepoInterface", file: str):
        return fem_interface.write(self, file)


@dataclass
class PhysicalFEM(FEM):
    unit: Optional[Literal["SI", "US", "ING"]] = "SI"
