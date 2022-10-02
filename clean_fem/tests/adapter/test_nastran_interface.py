from app.adapter.nastran_interface import NastranInterface
from app.domain.fem import FEM, Node


def test_nastran_load():
    with open("nastran_example.bdf", "w") as f:
        f.write("1, 12.3, 5.40, -3e-1\n")
        f.write("2, -10., 5.30, 8.2\n")
    ni = NastranInterface()
    model = FEM()
    model.load(ni, "nastran_example.bdf")
    assert model.nodes == {
        1: Node(id=1, x=12.3, y=5.4, z=-0.3),
        2: Node(id=2, x=-10.0, y=5.3, z=8.2),
    }
