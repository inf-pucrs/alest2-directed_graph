
from collections import deque
from dataclasses import astuple, dataclass, field
from itertools import filterfalse
from typing import Dict, List, Mapping, Set, Tuple, TypeVar, Union


Vertex = str
Edge = Tuple[Vertex, Vertex]

Number = Union[int, float]
T = TypeVar("T", Vertex, str)


@dataclass(order=True, frozen=True)
class WeightedEdge:
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


@dataclass(order=True, frozen=True)
class DirGraph:
    def __init__(self, adjacency_dict: Dict[Vertex, Set[Edge]]):
        super().__init__()
        self.adjacency_dict = dict(adjacency_dict)
        self.marks: Dict[Vertex, bool] = {}
        self.in_use: Dict[Vertex, bool] = {}

    def mark(self, vertex: Vertex):
        self.marks[vertex] = True

    def is_marked(self, vertex: Vertex) -> bool:
        return self.marks.get(vertex, False)

    def unmark_all(self):
        self.marks = {}

    def __len__(self) -> int:
        return len(self.adjacency_dict)
    
    def get_edges(self) -> Set[Edge]:
        edges = {
            edge
            for node, edges in self.adjacency_dict.items()
            for edge in edges
        }
        return edges
    
    def get_neighbors(self, vertex: Vertex) -> Set[Vertex]:
        neighbors = {head for tail, head in self.adjacency_dict[vertex]}
        return neighbors

    def get_nodes_in_use(self) -> List[Vertex]:
        return list(self.in_use.keys())

    def add_edge(self, tail: Vertex, head: Vertex):
        self.adjacency_dict[tail].add((tail, head))

    def remove_edge(self, tail: Vertex, head: Vertex):
        self.adjacency_dict[tail].remove((tail, head))
    
    def __repr__(self):
        return repr(self.adjacency_dict)

    def get_all_degrees(self) -> Dict[Vertex, int]:
        """
        Get the number of edges that point to each node.
        
        O(2V + E)
        """
        in_degrees_counter = {
            vertex: 0 for vertex in self.adjacency_dict.keys()
        }
        for out_edges in self.adjacency_dict.values():
            for _, head in out_edges:
                in_degrees_counter[head] += 1
        return in_degrees_counter

    def breadth_first_walk(self, node: Vertex) -> None:
        queue = deque()
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
        "a": {("a", "b"), ("a", "c")},
        "b": {("b", "a")},
        "c": {},
        "d": {("d", "a")},
    }
    graph = DirGraph(adj_dict)
    print(graph)
    print(graph.get_edges())
    print(graph.get_all_degrees())
    graph.breadth_first_walk("a")
    print(graph.marks)
