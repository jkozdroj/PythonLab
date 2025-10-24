
from typing import Dict, List, Tuple, Hashable, Optional
import heapq

Node = Hashable
Graph = Dict[Node, List[Tuple[Node, float]]]

def dijkstra(graph: Graph, source: Node, target: Optional[Node] = None):
    dist: Dict[Node, float] = {source: 0.0}
    prev: Dict[Node, Optional[Node]] = {source: None}
    pq: List[Tuple[float, Node]] = [(0.0, source)]  # (odległość, węzeł)

    visited = set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)

        if target is not None and u == target:
            break

        for v, w in graph.get(u, []):
            if w < 0:
                raise ValueError("Dijkstra wymaga nieujemnych wag krawędzi.")
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    return dist, prev

def reconstruct_path(prev: Dict[Node, Optional[Node]], target: Node) -> List[Node]:
    if target not in prev:
        return []
    path = []
    cur: Optional[Node] = target
    while cur is not None:
        path.append(cur)
        cur = prev.get(cur)
    path.reverse()
    return path

# --- Przykład użycia ---
if __name__ == "__main__":
    # Graf skierowany: A->B(4), A->C(2), C->B(1), B->D(5), C->D(8), D->E(6)
    graph: Graph = {
        "A": [("B", 4), ("C", 2)],
        "B": [("D", 5)],
        "C": [("B", 1), ("D", 8)],
        "D": [("E", 6)],
        "E": [],
    }

    dist, prev = dijkstra(graph, source="A", target="E")
    path = reconstruct_path(prev, "E")
    print("Dystanse:", dist)     # {'A': 0.0, 'C': 2.0, 'B': 3.0, 'D': 8.0, 'E': 14.0}
    print("Ścieżka A→E:", path)  # ['A', 'C', 'B', 'D', 'E']
