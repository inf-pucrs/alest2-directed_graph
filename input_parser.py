
from collections import defaultdict
from pathlib import Path
from typing import Dict, Set

from graph import DirGraph


def read_file(filepath: Path) -> str:
    with open(filepath) as text_file:
        return text_file.read()


def text_to_adjancency_dict(text: str) -> Dict[str, Set[str]]:
    adj_dict = defaultdict(set)
    for line in text.split("\n"):
        tail, head = line.split()
        if tail == "0" and head == "0":
            break
        adj_dict[tail].add(head)        
    return adj_dict


def read_graph_from_file(file_path: Path = Path("./examples.txt")):
    lines = read_file(file_path)
    adj_dict = text_to_adjancency_dict(lines)
    return DirGraph(adj_dict)


if __name__ == "__main__":
    print(read_graph_from_file())
