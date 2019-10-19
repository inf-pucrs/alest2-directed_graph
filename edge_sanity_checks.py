
from itertools import starmap

from graph import WeightedEdge


edges = [("", "", 5), ("", "", 15), ("", "", 2), ("", "", 16), ("", "", 3)]
edges = starmap(WeightedEdge, edges)
print(sorted(edges))

edges = [("a", "b", 5), ("a", "a", 15), ("b", "a", 2), ("a", "d", 16)]
edges = starmap(WeightedEdge, edges)
print(sorted(edges))

edges = [("a", "b", 5), ("a", "b", 15), ("b", "a", 2), ("a", "d", 2)]
edges = starmap(WeightedEdge, edges)
print(set(edges))

ed, ge = WeightedEdge("b", "a", 2), WeightedEdge("a", "d", 2)
print(ed == ge, ed != ge)
print(hash(ed), hash(ge))

ed, ge = WeightedEdge("b", "a", 2), WeightedEdge("b", "a", 2)
print(ed == ge, ed != ge)
print(hash(ed), hash(ge))
