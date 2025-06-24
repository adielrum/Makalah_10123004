#!/usr/bin/env python3
"""
Graph data model for vertex cover visualization
"""

from typing import Set, List, Tuple, Optional
from dataclasses import dataclass

@dataclass(frozen=True)
class Vertex:
    """Represents a vertex in the graph"""
    id: int
    x: float = 0.0
    y: float = 0.0
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if isinstance(other, Vertex):
            return self.id == other.id
        return False

@dataclass(frozen=True)
class Edge:
    """Represents an edge in the graph"""
    u: Vertex
    v: Vertex
    
    def __post_init__(self):
        # Ensure consistent ordering for undirected edges
        if self.u.id > self.v.id:
            object.__setattr__(self, 'u', self.v)
            object.__setattr__(self, 'v', self.u)
    
    def __hash__(self):
        return hash((self.u, self.v))
    
    def __eq__(self, other):
        if isinstance(other, Edge):
            return (self.u == other.u and self.v == other.v) or \
                   (self.u == other.v and self.v == other.u)
        return False
    
    def contains_vertex(self, vertex: Vertex) -> bool:
        """Check if edge contains the given vertex"""
        return self.u == vertex or self.v == vertex
    
    def get_other_vertex(self, vertex: Vertex) -> Optional[Vertex]:
        """Get the other vertex of the edge"""
        if self.u == vertex:
            return self.v
        elif self.v == vertex:
            return self.u
        return None

class Graph:
    """Graph data structure for vertex cover algorithms"""
    
    def __init__(self):
        self._vertices: Set[Vertex] = set()
        self._edges: Set[Edge] = set()
        self._next_vertex_id = 1
    
    def add_vertex(self, x: float = 0.0, y: float = 0.0) -> Vertex:
        """Add a new vertex to the graph"""
        vertex = Vertex(self._next_vertex_id, x, y)
        self._vertices.add(vertex)
        self._next_vertex_id += 1
        return vertex
    
    def add_edge(self, u: Vertex, v: Vertex) -> bool:
        """Add an edge between two vertices"""
        if u not in self._vertices or v not in self._vertices:
            return False
        if u == v:  # No self-loops
            return False
        
        # Ensure canonical order for edge creation
        if u.id > v.id:
            u, v = v, u # Swap to ensure u.id <= v.id
            
        edge = Edge(u, v)
        if edge not in self._edges:
            self._edges.add(edge)
            return True
        return False
    
    def remove_vertex(self, vertex: Vertex) -> bool:
        """Remove a vertex and all its incident edges"""
        if vertex not in self._vertices:
            return False
        
        # Remove all incident edges
        incident_edges = self.get_incident_edges(vertex)
        for edge in incident_edges:
            self._edges.remove(edge)
        
        self._vertices.remove(vertex)
        return True
    
    def remove_edge(self, edge: Edge) -> bool:
        """Remove an edge from the graph"""
        if edge in self._edges:
            self._edges.remove(edge)
            return True
        return False
    
    def get_vertices(self) -> Set[Vertex]:
        """Get all vertices in the graph"""
        return self._vertices.copy()
    
    def get_edges(self) -> Set[Edge]:
        """Get all edges in the graph"""
        return self._edges.copy()
    
    def get_incident_edges(self, vertex: Vertex) -> Set[Edge]:
        """Get all edges incident to a vertex"""
        return {edge for edge in self._edges if edge.contains_vertex(vertex)}
    
    def get_neighbors(self, vertex: Vertex) -> Set[Vertex]:
        """Get all neighbors of a vertex"""
        neighbors = set()
        for edge in self.get_incident_edges(vertex):
            other = edge.get_other_vertex(vertex)
            if other:
                neighbors.add(other)
        return neighbors
    
    def get_vertex_by_id(self, vertex_id: int) -> Optional[Vertex]:
        """Get vertex by its ID"""
        for vertex in self._vertices:
            if vertex.id == vertex_id:
                return vertex
        return None
    
    def get_vertex_at_position(self, x: float, y: float, tolerance: float = 20.0) -> Optional[Vertex]:
        """Get vertex at given position within tolerance"""
        for vertex in self._vertices:
            distance = ((vertex.x - x) ** 2 + (vertex.y - y) ** 2) ** 0.5
            if distance <= tolerance:
                return vertex
        return None
    
    def clear(self):
        """Clear all vertices and edges"""
        self._vertices.clear()
        self._edges.clear()
        self._next_vertex_id = 1
    
    def copy(self) -> 'Graph':
        """Create a copy of the graph"""
        new_graph = Graph()
        
        # Copy vertices
        vertex_mapping = {}
        for vertex in self._vertices:
            new_vertex = Vertex(vertex.id, vertex.x, vertex.y)
            new_graph._vertices.add(new_vertex)
            vertex_mapping[vertex] = new_vertex
        
        # Copy edges
        for edge in self._edges:
            new_u = vertex_mapping[edge.u]
            new_v = vertex_mapping[edge.v]
            new_graph._edges.add(Edge(new_u, new_v))
        
        new_graph._next_vertex_id = self._next_vertex_id
        return new_graph
    
    def __len__(self) -> int:
        """Return number of vertices"""
        return len(self._vertices)
    
    def __str__(self) -> str:
        """String representation of the graph"""
        return f"Graph(vertices={len(self._vertices)}, edges={len(self._edges)})"