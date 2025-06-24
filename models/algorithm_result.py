#!/usr/bin/env python3
"""
Algorithm result data structures for vertex cover visualization
"""

from typing import Set, Optional
from dataclasses import dataclass
from .graph import Vertex, Edge

@dataclass
class StepResult:
    """Result of a single algorithm step"""
    vertex_cover_so_far: Set[Vertex]
    remaining_edges: Set[Edge]
    message: str
    selected_edge: Optional[Edge] = None
    added_vertices: Optional[Set[Vertex]] = None
    removed_edges: Optional[Set[Edge]] = None
    
    def __post_init__(self):
        if self.added_vertices is None:
            self.added_vertices = set()
        if self.removed_edges is None:
            self.removed_edges = set()

@dataclass
class VertexCoverResult:
    """Final result of vertex cover algorithm"""
    vertex_cover: Set[Vertex]
    total_steps: int
    algorithm_name: str
    is_optimal: bool = False
    approximation_ratio: Optional[float] = None
    time_taken: Optional[float] = None
    
    def __str__(self) -> str:
        result = f"Algorithm: {self.algorithm_name}\n"
        result += f"Vertex Cover Size: {len(self.vertex_cover)}\n"
        result += f"Total Steps: {self.total_steps}\n"
        if self.approximation_ratio:
            result += f"Approximation Ratio: {self.approximation_ratio}\n"
        if self.time_taken is not None:
            result += f"Time Taken: {self.time_taken:.4f} seconds\n"
        result += f"Vertices: {[v.id for v in self.vertex_cover]}"
        return result