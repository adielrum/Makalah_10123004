#!/usr/bin/env python3
"""
2-Approximation Algorithm for Vertex Cover

This algorithm provides a 2-approximation for the minimum vertex cover problem.
It works by repeatedly selecting an arbitrary edge and adding both its endpoints
to the vertex cover, then removing all edges incident to these vertices.
"""

from typing import Generator, Set
from models import Graph, Vertex, Edge, StepResult, VertexCoverResult

def run(graph: Graph) -> Generator[StepResult, None, VertexCoverResult]:
    """
    Run the 2-approximation algorithm for vertex cover
    
    Args:
        graph: The input graph
        
    Yields:
        StepResult: Information about each step of the algorithm
        
    Returns:
        VertexCoverResult: Final result of the algorithm
    """
    # Initialize
    vertex_cover = set()
    remaining_edges = graph.get_edges().copy()
    step_count = 0
    
    # Initial step
    yield StepResult(
        vertex_cover_so_far=vertex_cover.copy(),
        remaining_edges=remaining_edges.copy(),
        message="Starting 2-Approximation Algorithm. Initialize empty vertex cover."
    )
    
    # Main algorithm loop
    while remaining_edges:
        step_count += 1
        
        # Pick an arbitrary edge
        selected_edge = next(iter(remaining_edges))
        u, v = selected_edge.u, selected_edge.v
        
        # Show edge selection
        yield StepResult(
            vertex_cover_so_far=vertex_cover.copy(),
            remaining_edges=remaining_edges.copy(),
            message=f"Step {step_count}: Selected edge ({u.id}, {v.id})",
            selected_edge=selected_edge
        )
        
        # Add both vertices to the vertex cover
        vertex_cover.add(u)
        vertex_cover.add(v)
        added_vertices = {u, v}
        
        # Find all edges incident to u or v
        edges_to_remove = set()
        for edge in remaining_edges:
            if edge.contains_vertex(u) or edge.contains_vertex(v):
                edges_to_remove.add(edge)
        
        # Remove all incident edges
        remaining_edges -= edges_to_remove
        
        # Show the result of this step
        yield StepResult(
            vertex_cover_so_far=vertex_cover.copy(),
            remaining_edges=remaining_edges.copy(),
            message=f"Added vertices {u.id} and {v.id} to cover. Removed {len(edges_to_remove)} incident edges.",
            selected_edge=selected_edge,
            added_vertices=added_vertices,
            removed_edges=edges_to_remove
        )
    
    # Final step
    yield StepResult(
        vertex_cover_so_far=vertex_cover.copy(),
        remaining_edges=remaining_edges.copy(),
        message=f"Algorithm completed! Found vertex cover of size {len(vertex_cover)}."
    )
    
    # Return final result
    return VertexCoverResult(
        vertex_cover=vertex_cover,
        total_steps=step_count,
        algorithm_name="2-Approximation",
        is_optimal=False,
        approximation_ratio=2.0
    )

def get_algorithm_info() -> dict:
    """
    Get information about this algorithm
    
    Returns:
        dict: Algorithm metadata
    """
    return {
        "name": "2-Approximation",
        "description": "A 2-approximation algorithm for vertex cover that repeatedly selects edges and adds both endpoints to the cover.",
        "time_complexity": "O(E)",
        "approximation_ratio": 2.0,
        "optimal": False
    }