from app.domain.fem import FEM, Node, Element


def test_node_create():
    n = Node(12)
    assert n.id == 12
    n = Node(id=12, x=0.12, y=15)
    assert n.id == 12
    assert n.x == 0.12
    assert n.y == 15.0
    n = Node(id=12, x=0.12, y=15, z=-91e-2)
    assert n.id == 12
    assert n.x == 0.12
    assert n.y == 15.0
    assert n.z == -0.91


def test_element_create():
    nodeList = [1, 2, 3, 4]
    eid = 12
    e1 = Element(eid, nodeList)
    assert e1.id == eid
    assert e1.nodes == nodeList
    e2 = Element(id=eid, nodes=nodeList)
    assert e2.id == eid
    assert e2.nodes == nodeList


def test_element_contains_node():
    nodeList = [1, 2, 3, 4]
    eid = 12
    e = Element(eid, nodeList)
    for n in nodeList:
        assert n in e


def test_element_iter_nodes():
    nodeList = [1, 2, 3, 4]
    eid = 12
    e = Element(eid, nodeList)
    for n1, n2 in zip(e.nodes, nodeList):
        assert n1 == n2


def test_model_add_node():
    m = FEM()
    n = Node(12)
    m.add(n)
    assert n.id in m.nodes
    assert n in m


def test_model_add_element():
    m = FEM()
    e = Element(12, [1, 2, 3, 4])
    m.add(e)
    assert e.id in m.elements
    assert e in m


def test_create_model():
    model = FEM()
    elements = [[1, 2, 3], [2, 4, 3], [3, 4, 5]]
    for i, nodes in enumerate(elements):
        model.add(Element(i + 1, nodes))
        for nid in nodes:
            model.add(Node(nid))

    assert model.nodes == {
        1: Node(id=1),
        2: Node(id=2),
        3: Node(id=3),
        4: Node(id=4),
        5: Node(id=5),
    }
    assert model.elements == {
        1: Element(id=1, nodes=[1, 2, 3]),
        2: Element(id=2, nodes=[2, 4, 3]),
        3: Element(id=3, nodes=[3, 4, 5]),
    }
