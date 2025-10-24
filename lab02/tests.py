
import unittest

from tree import Tree, TreeNode


class TestTreeBasic(unittest.TestCase):
    def setUp(self):
        """
        Budujemy drzewo testowe:
        root
        +--(a) * A
        |   +--(1) * A1
        |   +--(2) * A2
        |       +--(->) * A2a
        +--(b) * B
            +--(x) * B1
                +--(*) * B1a
        +--(c) * C
            +--(c1) * C1
        """
        self.tree = Tree("root")
        a = self.tree.root.add_child("A", edge_value="a")
        b = self.tree.root.add_child("B", edge_value="b")
        a1 = a.add_child("A1", edge_value=1)
        a2 = a.add_child("A2", edge_value=2)
        a2a = a2.add_child("A2a", edge_value="->")
        b1 = b.add_child("B1", edge_value="x")
        b1a = b1.add_child("B1a", edge_value="*")
        # add_path od korzenia:
        self.tree.add_path(values=["C", "C1"], edges=["c", "c1"])

        # Zachowaj referencje dla czytelności w innych testach
        self.nodes = dict(root=self.tree.root, A=a, B=b, A1=a1, A2=a2, A2a=a2a, B1=b1, B1a=b1a)

    # --- Konstrukcja / wartości ---
    def test_root_value(self):
        self.assertEqual(self.tree.root.value, "root")

    def test_add_child_stores_node_and_edge_value(self):
        node = TreeNode("X")
        child = node.add_child("Y", edge_value="edgeY")
        self.assertEqual(node._children[0][0], "edgeY")   # wartość krawędzi
        self.assertIsInstance(node._children[0][1], TreeNode)
        self.assertEqual(node._children[0][1].value, "Y")  # wartość węzła dziecka

    def test_add_path_builds_chain_from_root(self):
        t = Tree("R")
        t.add_path(values=["V1", "V2"], edges=["e1", "e2"])
        # R --e1--> V1 --e2--> V2
        first_edge, first_child = t.root._children[0]
        self.assertEqual(first_edge, "e1")
        self.assertEqual(first_child.value, "V1")
        second_edge, second_child = first_child._children[0]
        self.assertEqual(second_edge, "e2")
        self.assertEqual(second_child.value, "V2")

    # --- Traversale ---
    def test_dfs_order(self):
        # preorder: root, A, A1, A2, A2a, B, B1, B1a, C, C1
        got = [n.value for n in self.tree.traverse_dfs()]
        expected = ["root", "A", "A1", "A2", "A2a", "B", "B1", "B1a", "C", "C1"]
        self.assertEqual(got, expected)

    def test_bfs_order(self):
        # warstwami: root | A, B, C | A1, A2, B1, C1 | A2a, B1a
        got = [n.value for n in self.tree.traverse_bfs()]
        expected = ["root", "A", "B", "C", "A1", "A2", "B1", "C1", "A2a", "B1a"]
        self.assertEqual(got, expected)

    def test_edges_listing(self):
        # sprawdź pary (parent, edge, child) w przewidywalnej kolejności DFS-owej
        edges = [(p.value, e, c.value) for (p, e, c) in self.tree.traverse_edges()]
        # Nie porównujemy całej listy „na sztywno” (mogą być zmiany w kolejności), ale sprawdzimy kilka kluczowych:
        self.assertIn(("root", "a", "A"), edges)
        self.assertIn(("root", "b", "B"), edges)
        self.assertIn(("A", 1, "A1"), edges)
        self.assertIn(("A", 2, "A2"), edges)
        self.assertIn(("A2", "->", "A2a"), edges)
        self.assertIn(("B", "x", "B1"), edges)
        # Krawędź bez None (tu akurat używamy "*" i żadnej None w setUp dla widoczności)
        self.assertIn(("B1", "*", "B1a"), edges)
        self.assertIn(("root", "c", "C"), edges)
        self.assertIn(("C", "c1", "C1"), edges)

    # --- __str__ / formatowanie ---
    def test_str_contains_node_values(self):
        s = str(self.tree)
        for val in ["root", "A", "A1", "A2", "A2a", "B", "B1", "B1a", "C", "C1"]:
            self.assertIn(val, s)

    def test_str_contains_edge_labels(self):
        s = str(self.tree)
        # Wersja ASCII używa "+--(edge) * value"
        for edge in ["a", "b", 1, 2, "->", "x", "*", "c", "c1"]:
            self.assertIn(f"({edge})", s)

    # --- Zachowanie pustego / jednowęzłowego drzewa ---
    def test_single_node_tree(self):
        t = Tree("only")
        # DFS/BFS zwracają tylko korzeń
        self.assertEqual([n.value for n in t.traverse_dfs()], ["only"])
        self.assertEqual([n.value for n in t.traverse_bfs()], ["only"])
        # edges() puste
        self.assertEqual(list(t.traverse_edges()), [])
        # __str__ zawiera tylko wartość korzenia
        self.assertEqual(str(t).strip(), "* only")


if __name__ == "__main__":
    unittest.main()
