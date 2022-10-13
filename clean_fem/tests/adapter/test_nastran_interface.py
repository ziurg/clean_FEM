from app.adapter.nastran_interface import NastranInterface
from app.domain.fem import FEM, Node, Element


def test_nastran_load():
    with open("nastran_example.bdf", "w") as f:
        f.write("GRID    12              0.12    15      -0.91   \n")
        f.write("GRID    13              -16.0   -4      0.0     \n")
        f.write("GRID    14              8.4     15      3.2     \n")
        f.write("CTRIA3  1               12      13      14      \n")
    ni = NastranInterface()
    model = FEM()
    model.load(ni, "nastran_example.bdf")
    assert model.nodes == {
        12: Node(id=12, x=0.12, y=15.0, z=-0.91),
        13: Node(id=13, x=-16.0, y=-4.0, z=0.0),
        14: Node(id=14, x=8.4, y=15.0, z=3.2),
    }
    assert model.elements == {1: Element(id=1, nodes=[12, 13, 14])}


def test_nastran_write():
    # Given an FEM Model and a nastran interface
    model = FEM()
    model.add(Node(id=12, x=0.12, y=15, z=-91e-2))
    model.add(Node(id=13, x=-16.0, y=-4, z=0.0))
    model.add(Node(id=14, x=8.40e2, y=15, z=3.2))
    model.add(Element(1, [12, 13, 14]))
    ni = NastranInterface()
    # When we ask to write the model
    model.write(ni, "nastran_example.bdf")
    # Then a corresponding file is written
    with open("nastran_example.bdf", "r") as f:
        lines = [line for line in f.readlines()]
        assert lines[0] == "GRID    12              0.12    15      -0.91   \n"
        assert lines[1] == "GRID    13              -16.0   -4      0.0     \n"
        assert lines[2] == "GRID    14              840.0   15      3.2     \n"
        assert lines[3] == "CTRIA3  1               12      13      14      \n"
