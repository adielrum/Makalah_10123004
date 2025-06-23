#!/usr/bin/env python3
"""
Brute-Force Algorithm for Vertex Cover

This algorithm provides an optimal solution for the minimum vertex cover problem
by exhaustively checking every possible subset of vertices. It is guaranteed to
find the smallest vertex cover, but it is extremely slow for larger graphs.
"""

from typing import Generator, Set
from itertools import combinations
from models import Graph, Vertex, Edge, StepResult, VertexCoverResult

def _is_vertex_cover(graph: Graph, vertex_subset: Set[Vertex]) -> bool:
    """
    Checks if a given subset of vertices constitutes a valid vertex cover.
    
    A subset is a vertex cover if for every edge in the graph, at least one
    of its endpoints is included in the subset.
    
    Args:
        graph: The graph to check against.
        vertex_subset: The subset of vertices to validate.
        
    Returns:
        True if the subset is a vertex cover, False otherwise.
    """
    for edge in graph.get_edges():
        if edge.u not in vertex_subset and edge.v not in vertex_subset:
            return False  # This edge is not covered
    return True

def run(graph: Graph) -> Generator[StepResult, None, VertexCoverResult]:
    """
    Run the brute-force algorithm for vertex cover.
    
    It iterates through all possible subset sizes (from 0 to N), generates
    all combinations of vertices for each size, and checks if any of them
    is a vertex cover. The first one found is guaranteed to be minimal.
    
    Args:
        graph: The input graph.
        
    Yields:
        StepResult: Information about each step of the algorithm for visualization.
        
    Returns:
        VertexCoverResult: The final, optimal result of the algorithm.
    """
    # Get all vertices and sort them to ensure consistent combination ordering
    all_vertices = sorted(list(graph.get_vertices()), key=lambda v: v.id)
    num_vertices = len(all_vertices)
    step_count = 0

    # Initial step to inform the user
    yield StepResult(
        vertex_cover_so_far=set(),
        remaining_edges=graph.get_edges().copy(),
        message="Starting Brute Force Algorithm. This may be very slow."
    )

    # Iterate through all possible subset sizes, from 0 to N
    for k in range(num_vertices + 1):
        step_count += 1
        yield StepResult(
            vertex_cover_so_far=set(),  # No cover found yet
            remaining_edges=graph.get_edges().copy(),
            message=f"Step {step_count}: Checking all subsets of size {k}..."
        )

        # Generate all combinations of vertices of size k
        for subset_tuple in combinations(all_vertices, k):
            current_subset = set(subset_tuple)
            step_count += 1
            
            # Yield a step to visualize which subset is currently being tested
            yield StepResult(
                vertex_cover_so_far=set(),  # Not a valid cover yet, just for viz
                remaining_edges=graph.get_edges().copy(),
                message=f"Step {step_count}: Testing subset: {[v.id for v in current_subset]}",
                added_vertices=current_subset  # Use this field to highlight the set
            )

            # Check if this subset is a valid vertex cover
            if _is_vertex_cover(graph, current_subset):
                # Since we are iterating by size, the first one found is the smallest
                final_message = f"Found optimal vertex cover of size {len(current_subset)}."
                yield StepResult(
                    vertex_cover_so_far=current_subset,
                    remaining_edges=set(),  # All edges are covered
                    message=final_message,
                    added_vertices=current_subset
                )
                
                # Return the final result, terminating the generator
                return VertexCoverResult(
                    vertex_cover=current_subset,
                    total_steps=step_count,
                    algorithm_name="Brute Force",
                    is_optimal=True,
                    approximation_ratio=1.0
                )
    
    # This part should only be reached if the graph has no edges.
    # The set of all vertices is always a cover for graphs with edges.
    yield StepResult(
        vertex_cover_so_far=set(),
        remaining_edges=set(),
        message="Algorithm completed. No edges to cover."
    )
    return VertexCoverResult(
        vertex_cover=set(),
        total_steps=step_count,
        algorithm_name="Brute Force",
        is_optimal=True,
        approximation_ratio=1.0
    )

def get_algorithm_info() -> dict:
    """
    Get information and metadata about this algorithm.
    
    Returns:
        A dictionary containing algorithm details.
    """
    return {
        "name": "Brute Force",
        "description": "An exhaustive search algorithm that checks every possible vertex subset to find the optimal vertex cover. Warning: Very slow for graphs with more than ~15 vertices.",
        "time_complexity": "O(2^V * E)",
        "approximation_ratio": 1.0,
        "optimal": True
    }