#!/usr/bin/env python3
"""
Greedy Algorithm for Vertex Cover

This algorithm uses a greedy approach by repeatedly selecting the vertex
with the highest degree (most incident edges) and adding it to the vertex cover.
"""

from typing import Generator, Set
from models import Graph, Vertex, Edge, StepResult, VertexCoverResult

def run(graph: Graph) -> Generator[StepResult, None, VertexCoverResult]:
    """
    Run the greedy algorithm for vertex cover
    
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
        message="Starting Greedy Algorithm. Initialize empty vertex cover."
    )
    
    # Main algorithm loop
    while remaining_edges:
        step_count += 1
        
        # Find vertex with highest degree among remaining edges
        vertex_degrees = {}
        for edge in remaining_edges:
            vertex_degrees[edge.u] = vertex_degrees.get(edge.u, 0) + 1
            vertex_degrees[edge.v] = vertex_degrees.get(edge.v, 0) + 1
        
        if not vertex_degrees:
            break
            
        # Select vertex with maximum degree
        selected_vertex = max(vertex_degrees.keys(), key=lambda v: vertex_degrees[v])
        max_degree = vertex_degrees[selected_vertex]
        
        # Show vertex selection
        yield StepResult(
            vertex_cover_so_far=vertex_cover.copy(),
            remaining_edges=remaining_edges.copy(),
            message=f"Step {step_count}: Selected vertex {selected_vertex.id} with degree {max_degree}",
            added_vertices={selected_vertex}
        )
        
        # Add vertex to the vertex cover
        vertex_cover.add(selected_vertex)
        
        # Find all edges incident to the selected vertex
        edges_to_remove = set()
        for edge in remaining_edges:
            if edge.contains_vertex(selected_vertex):
                edges_to_remove.add(edge)
        
        # Remove all incident edges
        remaining_edges -= edges_to_remove
        
        # Show the result of this step
        yield StepResult(
            vertex_cover_so_far=vertex_cover.copy(),
            remaining_edges=remaining_edges.copy(),
            message=f"Added vertex {selected_vertex.id} to cover. Removed {len(edges_to_remove)} incident edges.",
            added_vertices={selected_vertex},
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
        algorithm_name="Greedy",
        is_optimal=False,
        approximation_ratio=None  # Greedy doesn't have a guaranteed approximation ratio
    )

def get_algorithm_info() -> dict:
    """
    Get information about this algorithm
    
    Returns:
        dict: Algorithm metadata
    """
    return {
        "name": "Greedy",
        "description": "A greedy algorithm that repeatedly selects the vertex with the highest degree.",
        "time_complexity": "O(V * E)",
        "approximation_ratio": None,
        "optimal": False
    }