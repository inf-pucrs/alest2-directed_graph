
from collections import deque
from dataclasses import astuple, dataclass, field
from functools import partial
from itertools import filterfalse, starmap
from typing import Deque, Dict, Generic, List, Mapping, Set, Tuple, TypeVar, Union

from toolz import compose
from toolz.dicttoolz import valmap


Vertex = str
Number = Union[int, float]

T = TypeVar("T", Vertex, str)
EdgeAsTuple = Tuple[Vertex, Vertex, Number]


@dataclass(order=True, frozen=True)
class WeightedEdge(Generic[T]):
    tail: T = field(hash=True, compare=False)
    head: T = field(hash=True, compare=False)
    weight: Number

    def __eq__(self, other):
        """
        Must research difference among
        isinstance(self, type(other))
        isinstance(other, type(self))
        type(self) is type(other)
        """
        if isinstance(self, type(other)):
            if astuple(self) == astuple(other):
                return True
        else:
            return NotImplemented
        return False

        def __ne__(self, other):
            return not self == other


class DirGraph:
    def __init__(self, adjacency_dict: Mapping[Vertex, Set[EdgeAsTuple]]):
        super().__init__()
        self.adjacencies = valmap(
            compose(set, partial(starmap, WeightedEdge)),
            adjacency_dict,
        )
        self.marks: Dict[Vertex, bool] = {}
        self.in_use: Dict[Vertex, bool] = {}

    def mark(self, vertex: Vertex):
        self.marks[vertex] = True

    def is_marked(self, vertex: Vertex) -> bool:
        return self.marks.get(vertex, False)

    def unmark_all(self):
        self.marks = {}

    def __len__(self) -> int:
        return len(self.adjacencies)

    def get_edges(self) -> Set[WeightedEdge]:
        edges = {
            edge
            for node, edges in self.adjacencies.items()
            for edge in edges
        }
        return edges

    def get_neighbors(self, vertex: Vertex) -> Set[Vertex]:
        neighbors = {edge.head for edge in self.adjacencies[vertex]}
        return neighbors

    def get_nodes_in_use(self) -> List[Vertex]:
        return list(self.in_use.keys())

    def add_edge(self, tail: Vertex, head: Vertex, weight: Number):
        self.adjacencies[tail].add(WeightedEdge(tail, head, Number))

    def remove_edge(self, tail: Vertex, head: Vertex, weight: Number):
        self.adjacencies[tail].remove(WeightedEdge(tail, head, Number))

    def __repr__(self):
        return repr(self.adjacencies)

    def get_all_degrees(self) -> Dict[Vertex, int]:
        """
        Get the number of edges that point to each node.

        O(2V + E)
        """
        in_degrees_counter = {
            vertex: 0 for vertex in self.adjacencies.keys()
        }
        for out_edges in self.adjacencies.values():
            for edge in out_edges:
                in_degrees_counter[edge.head] += 1
        return in_degrees_counter

    def breadth_first_walk(self, node: Vertex) -> None:
        queue: Deque[Vertex] = deque()
        queue.append(node)
        while queue:
            vertex = queue.popleft()
            self.marks[vertex] = True
            neighbors = self.get_neighbors(vertex)
            unmarked_nodes = filterfalse(self.is_marked, neighbors)
            queue.extend(unmarked_nodes)

    def get_minimum_spanning_tree_kruskal(self):
        pass


if __name__ == "__main__":

    adj_dict = {
        "a": {("a", "b", 5), ("a", "c", 4)},
        "b": {("b", "a", 3)},
        "c": {},
        "d": {("d", "a", 6)},
    }
    graph = DirGraph(adj_dict)
    print(graph)
    print(graph.get_edges())
    print(graph.get_all_degrees())
    graph.breadth_first_walk("a")
    print(graph.marks)
