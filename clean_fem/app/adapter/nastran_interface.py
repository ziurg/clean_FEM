from app.domain.fem import FEM, Node
from app.domain.fem_loader import Loader


class NastranInterface(Loader):
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
            for line in f.readlines():
                [id, x, y, z, *_] = line.split(",")
                n = Node(id=int(id), x=float(x), y=float(y), z=float(z))
                model.add(n)
        return model
