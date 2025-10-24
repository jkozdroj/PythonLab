# -*- coding: utf-8 -*-
from collections import deque
from typing import Any, List, Tuple, Iterable, Generator, Optional

class TreeNode:
    """
    Wezel drzewa:
    - value: wartosc w wezle
    - _children: lista par (edge_value, child_node)
    """
    __slots__ = ("value", "_children")

    def __init__(self, value: Any):
        self.value = value
        self._children: List[Tuple[Any, "TreeNode"]] = []

    def add_child(self, child_value: Any, edge_value: Any = None) -> "TreeNode":
        child = TreeNode(child_value)
        self._children.append((edge_value, child))
        return child

    def children(self) -> Iterable[Tuple[Any, "TreeNode"]]:
        return iter(self._children)

    # Przechodzenia od TEGO wezla
    def dfs(self) -> Generator["TreeNode", None, None]:
        yield self
        for _, ch in self._children:
            yield from ch.dfs()

    def bfs(self) -> Generator["TreeNode", None, None]:
        q = deque([self])
        while q:
            node = q.popleft()
            yield node
            for _, ch in node._children:
                q.append(ch)

    def edges(self) -> Generator[Tuple["TreeNode", Any, "TreeNode"], None, None]:
        for edge_val, ch in self._children:
            yield (self, edge_val, ch)
            yield from ch.edges()

    # Formatowanie w czystym ASCII
    def _format_ascii(self, prefix: str = "", is_last: bool = True) -> List[str]:
        """
        Zwraca linie ASCII dla poddrzewa.
        Wezel: "* value"
        Dziecko: "+--(edge) * child" lub "+-- * child"
        Prefiksy dla galezi: "|   " i "    "
        """
        node_label = "* " + str(self.value)
        lines = [node_label]

        child_count = len(self._children)
        for idx, (edge_val, ch) in enumerate(self._children):
            last = (idx == child_count - 1)
            branch = "+--"
            edge_label = "(" + str(edge_val) + ") " if edge_val is not None else ""
            # naglówek dziecka
            child_lines = ch._format_ascii(prefix="", is_last=last)
            head = prefix + branch + edge_label + child_lines[0]
            lines.append(head)
            # reszta poddrzewa z odpowiednim prefiksem
            child_prefix = prefix + ("    " if last else "|   ")
            for sub in child_lines[1:]:
                lines.append(child_prefix + sub)
        return lines


class Tree:
    def __init__(self, root_value: Any):
        self.root = TreeNode(root_value)

    def add_path(self, values: List[Any], edges: Optional[List[Any]] = None) -> None:
        node = self.root
        for i, val in enumerate(values):
            edge_val = None
            if edges is not None and i < len(edges):
                edge_val = edges[i]
            node = node.add_child(val, edge_value=edge_val)

    def traverse_dfs(self) -> Generator[TreeNode, None, None]:
        yield from self.root.dfs()

    def traverse_bfs(self) -> Generator[TreeNode, None, None]:
        yield from self.root.bfs()

    def traverse_edges(self) -> Generator[Tuple[TreeNode, Any, TreeNode], None, None]:
        yield from self.root.edges()

    def __str__(self) -> str:
        return "\n".join(self.root._format_ascii())


# ===== DEMO =====
if __name__ == "__main__":
    tree = Tree("root")
    a = tree.root.add_child("A", edge_value="a")
    b = tree.root.add_child("B", edge_value="b")
    a1 = a.add_child("A1", edge_value=1)
    a2 = a.add_child("A2", edge_value=2)
    b1 = b.add_child("B1", edge_value="x")
    a2.add_child("A2a", edge_value="->")
    b1.add_child("B1a", edge_value=None)
    tree.add_path(values=["C", "C1"], edges=["c", "c1"])

    print("== DRZEWO ==")
    print(tree)

    print("\n== DFS ==")
    print([n.value for n in tree.traverse_dfs()])

    print("\n== BFS ==")
    print([n.value for n in tree.traverse_bfs()])

    print("\n== KRAWEDZIE ==")
    for parent, edge, child in tree.traverse_edges():
        label = edge if edge is not None else "None"
        print(f"{parent.value} --{label}--> {child.value}")
