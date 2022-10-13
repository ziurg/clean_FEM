from typing import List, Any
from app.domain.fem import FEM, Node, Element
from app.domain.fem_repo_interface import RepoInterface


def writeBy8(items: List[Any]) -> str:
    def by8(text):
        return "{:<8}".format(text)

    return "".join(map(by8, items))


def splitBy8(text: str, chunk_size: int = 8) -> List[str]:
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


class NastranNode(Node):
    def __init__(self, n: Node):
        super().__init__(**vars(n))

    def __repr__(self):
        # GRID    1               0.      0.      0.              3456
        return writeBy8(["GRID", self.id, "", self.x, self.y, self.z]) + "\n"


class NastranElement(Element):
    def __init__(self, e: Element):
        super().__init__(**vars(e))

    def __repr__(self):
        if len(self.nodes) == 3:
            text = writeBy8(
                ["CTRIA3", self.id, "", self.nodes[0], self.nodes[1], self.nodes[2]]
            )
            text += "\n"
            return text
        else:
            raise NotImplementedError("This can of element is not yet implemented.")


class NastranInterface(RepoInterface):
    def load(self, model: FEM, file: str) -> FEM:
        """Read an MSC Nastran bulk file

        Args:
            file (str): path to the file to parse.

        Returns:
            FEM: Finite Element Model

        Notes:
            This is a function example not really loading Nastran
            files, but only files with nodes written in the
            following format :
            1, 12.3, 5.4, -0.3
            2, -10., 5.3, 8.2
        """
        with open(file, "r") as f:
            lines = (line.strip() for line in f.readlines())
            lines = (line for line in lines if line)
            for line in lines:
                fields = map(str.strip, splitBy8(line))
                [name, field1, _, field3, field4, field5, *_] = fields
                if name == "GRID":
                    item = Node(
                        id=int(field1),
                        x=float(field3),
                        y=float(field4),
                        z=float(field5),
                    )
                elif name == "CTRIA3":
                    item = Element(
                        id=int(field1), nodes=[int(field3), int(field4), int(field5)]
                    )
                model.add(item)
        return model

    def write(self, model: FEM, file: str) -> None:
        with open(file, "w") as f:
            for n in model.nodes.values():
                nx_node = NastranNode(n)
                f.write(str(nx_node))
            for e in model.elements.values():
                nx_elt = NastranElement(e)
                f.write(str(nx_elt))
