#!/usr/bin/env python3
"""
Example usage of the Vertex Cover Visualization Tool

This script demonstrates how to:
1. Create graphs programmatically
2. Run algorithms without the GUI
3. Analyze results
"""

from models import Graph
from algorithms import get_available_algorithms, run_algorithm, get_algorithm_info

def create_sample_graph() -> Graph:
    """Create a sample graph for testing"""
    graph = Graph()
    
    # Create vertices in a triangle formation
    v1 = graph.add_vertex(0, 0)      # Vertex 1 at (0, 0)
    v2 = graph.add_vertex(100, 0)    # Vertex 2 at (100, 0)
    v3 = graph.add_vertex(50, 100)   # Vertex 3 at (50, 100)
    v4 = graph.add_vertex(150, 50)   # Vertex 4 at (150, 50)
    
    # Create edges to form a connected graph
    graph.add_edge(v1, v2)  # Edge 1-2
    graph.add_edge(v2, v3)  # Edge 2-3
    graph.add_edge(v3, v1)  # Edge 3-1 (completes triangle)
    graph.add_edge(v2, v4)  # Edge 2-4
    graph.add_edge(v3, v4)  # Edge 3-4
    
    return graph

def create_star_graph(center_pos=(50, 50), num_arms=5) -> Graph:
    """Create a star graph with one central vertex connected to multiple outer vertices"""
    graph = Graph()
    
    # Create center vertex
    center = graph.add_vertex(center_pos[0], center_pos[1])
    
    # Create outer vertices and connect them to center
    import math
    radius = 80
    for i in range(num_arms):
        angle = 2 * math.pi * i / num_arms
        x = center_pos[0] + radius * math.cos(angle)
        y = center_pos[1] + radius * math.sin(angle)
        
        outer_vertex = graph.add_vertex(x, y)
        graph.add_edge(center, outer_vertex)
    
    return graph

def run_algorithm_demo(graph: Graph, algorithm_name: str):
    """Run an algorithm and display step-by-step results"""
    print(f"\n{'='*60}")
    print(f"Running {algorithm_name} Algorithm")
    print(f"{'='*60}")
    
    # Get algorithm info
    info = get_algorithm_info(algorithm_name)
    print(f"Description: {info['description']}")
    print(f"Time Complexity: {info['time_complexity']}")
    if info['approximation_ratio']:
        print(f"Approximation Ratio: {info['approximation_ratio']}")
    print(f"Optimal: {'Yes' if info['optimal'] else 'No'}")
    print()
    
    # Run algorithm
    algorithm_gen = run_algorithm(algorithm_name, graph)
    
    step_count = 0
    for step_result in algorithm_gen:
        step_count += 1
        print(f"Step {step_count}: {step_result.message}")
        
        if step_result.vertex_cover_so_far:
            vertex_ids = [v.id for v in step_result.vertex_cover_so_far]
            print(f"  Current vertex cover: {vertex_ids}")
        
        if step_result.selected_edge:
            edge = step_result.selected_edge
            print(f"  Selected edge: ({edge.u.id}, {edge.v.id})")
        
        if step_result.added_vertices:
            added_ids = [v.id for v in step_result.added_vertices]
            print(f"  Added vertices: {added_ids}")
        
        if step_result.removed_edges:
            print(f"  Removed {len(step_result.removed_edges)} edges")
        
        print(f"  Remaining edges: {len(step_result.remaining_edges)}")
        print()
    
    # The last iteration returns the final result
    try:
        final_result = algorithm_gen.gi_frame.f_locals.get('result')
        if hasattr(final_result, 'vertex_cover'):
            print(f"Final Result:")
            print(f"  Vertex Cover: {[v.id for v in final_result.vertex_cover]}")
            print(f"  Cover Size: {len(final_result.vertex_cover)}")
            print(f"  Total Steps: {final_result.total_steps}")
    except:
        pass

def compare_algorithms(graph: Graph):
    """Compare different algorithms on the same graph"""
    print(f"\n{'='*60}")
    print("Algorithm Comparison")
    print(f"{'='*60}")
    
    algorithms = get_available_algorithms()
    results = {}
    
    for algorithm_name in algorithms.keys():
        print(f"\nRunning {algorithm_name}...")
        
        # Run algorithm and collect final result
        algorithm_gen = run_algorithm(algorithm_name, graph)
        steps = list(algorithm_gen)
        
        # Extract final result
        try:
            # The generator should return the final result
            final_result = algorithm_gen.gi_frame.f_locals.get('result')
            if final_result:
                results[algorithm_name] = {
                    'cover_size': len(final_result.vertex_cover),
                    'steps': final_result.total_steps,
                    'vertices': [v.id for v in final_result.vertex_cover]
                }
        except:
            # Fallback: use the last step result
            if steps:
                last_step = steps[-1]
                results[algorithm_name] = {
                    'cover_size': len(last_step.vertex_cover_so_far),
                    'steps': len(steps),
                    'vertices': [v.id for v in last_step.vertex_cover_so_far]
                }
    
    # Display comparison
    print(f"\n{'Algorithm':<20} {'Cover Size':<12} {'Steps':<8} {'Vertices'}")
    print("-" * 60)
    
    for algorithm_name, result in results.items():
        vertices_str = str(result['vertices'])
        print(f"{algorithm_name:<20} {result['cover_size']:<12} {result['steps']:<8} {vertices_str}")

def main():
    """Main demonstration function"""
    print("Vertex Cover Visualization Tool - Example Usage")
    print("=" * 60)
    
    # Show available algorithms
    algorithms = get_available_algorithms()
    print(f"Available algorithms: {list(algorithms.keys())}")
    
    # Create and analyze sample graphs
    print("\n1. Triangle + Extension Graph")
    graph1 = create_sample_graph()
    print(f"Created graph with {len(graph1.get_vertices())} vertices and {len(graph1.get_edges())} edges")
    
    # Run each algorithm on the sample graph
    for algorithm_name in algorithms.keys():
        run_algorithm_demo(graph1, algorithm_name)
    
    # Compare algorithms
    compare_algorithms(graph1)
    
    print("\n2. Star Graph")
    graph2 = create_star_graph(num_arms=6)
    print(f"Created star graph with {len(graph2.get_vertices())} vertices and {len(graph2.get_edges())} edges")
    
    # Compare algorithms on star graph
    compare_algorithms(graph2)
    
    print("\n" + "="*60)
    print("Demo completed! To run the interactive GUI:")
    print("python main.py")
    print("="*60)

if __name__ == "__main__":
    main()