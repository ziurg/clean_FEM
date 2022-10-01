from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List, Optional, Literal
from functools import singledispatchmethod
from xmlrpc.client import Boolean

if TYPE_CHECKING:
    from app.domain.fem_repository import FEMRepository


@dataclass
class Element:
    id: int
    nodes: List[int]

    def __contains__(self, nid: int) -> Boolean:
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
    def add(self, item) -> None:
        raise NotImplementedError("This object type can't be added to the model.")

    @add.register(Node)
    def _(self, n: Node) -> None:
        self.nodes[n.id] = n

    @add.register(Element)
    def _(self, e: Element) -> None:
        self.elements[e.id] = e

    @singledispatchmethod
    def __contains__(self, item) -> Boolean:
        raise NotImplementedError("This object type is not valid for this method.")

    @__contains__.register(Node)
    def _(self, n: Node) -> Boolean:
        return n.id in self.nodes

    @__contains__.register(Element)
    def _(self, e: Element) -> Boolean:
        return e.id in self.elements

    def save(self, repo: "FEMRepository"):
        return repo.add(self)


@dataclass
class PhysicalFEM(FEM):
    unit: Optional[Literal["SI", "US", "ING"]] = "SI"
