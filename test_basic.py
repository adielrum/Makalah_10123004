#!/usr/bin/env python3
"""
Basic test script to verify the vertex cover visualization tool
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from models import Graph, Vertex, Edge, StepResult, VertexCoverResult
        print("✓ Models imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import models: {e}")
        return False
    
    try:
        from algorithms import get_available_algorithms, run_algorithm
        print("✓ Algorithms imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import algorithms: {e}")
        return False
    
    try:
        from PyQt6.QtWidgets import QApplication
        print("✓ PyQt6 imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import PyQt6: {e}")
        print("Please install PyQt6: pip install PyQt6")
        return False
    
    return True

def test_graph_operations():
    """Test basic graph operations"""
    print("\nTesting graph operations...")
    
    from models import Graph
    
    # Create graph
    graph = Graph()
    print("✓ Graph created")
    
    # Add vertices
    v1 = graph.add_vertex(10, 20)
    v2 = graph.add_vertex(30, 40)
    v3 = graph.add_vertex(50, 60)
    print(f"✓ Added 3 vertices: {v1.id}, {v2.id}, {v3.id}")
    
    # Add edges
    success1 = graph.add_edge(v1, v2)
    success2 = graph.add_edge(v2, v3)
    print(f"✓ Added edges: {success1}, {success2}")
    
    # Check graph state
    vertices = graph.get_vertices()
    edges = graph.get_edges()
    print(f"✓ Graph has {len(vertices)} vertices and {len(edges)} edges")
    
    return True

def test_algorithms():
    """Test algorithm loading and basic execution"""
    print("\nTesting algorithms...")
    
    from models import Graph
    from algorithms import get_available_algorithms, run_algorithm
    
    # Get available algorithms
    algorithms = get_available_algorithms()
    print(f"✓ Available algorithms: {list(algorithms.keys())}")
    
    # Create a simple graph
    graph = Graph()
    v1 = graph.add_vertex(0, 0)
    v2 = graph.add_vertex(100, 0)
    v3 = graph.add_vertex(50, 100)
    graph.add_edge(v1, v2)
    graph.add_edge(v2, v3)
    graph.add_edge(v1, v3)
    
    # Test 2-approximation algorithm
    if "2-Approximation" in algorithms:
        print("Testing 2-Approximation algorithm...")
        try:
            algorithm_gen = run_algorithm("2-Approximation", graph)
            steps = list(algorithm_gen)
            result = steps[-1] if steps else None
            print(f"✓ 2-Approximation completed with {len(steps)} steps")
            if hasattr(result, 'vertex_cover'):
                print(f"✓ Found vertex cover of size {len(result.vertex_cover)}")
        except Exception as e:
            print(f"✗ 2-Approximation failed: {e}")
            return False
    
    return True

def test_gui_creation():
    """Test GUI component creation (without showing)"""
    print("\nTesting GUI components...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from gui import MainWindow
        
        # Create application (required for Qt widgets)
        app = QApplication([])
        
        # Create main window (but don't show it)
        window = MainWindow()
        print("✓ Main window created successfully")
        
        # Test basic functionality
        print(f"✓ Window title: {window.windowTitle()}")
        print(f"✓ Graph canvas created: {window.graph_canvas is not None}")
        print(f"✓ Algorithm panel created: {window.algorithm_panel is not None}")
        
        # Clean up
        window.close()
        app.quit()
        
        return True
        
    except Exception as e:
        print(f"✗ GUI test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Vertex Cover Visualization Tool - Basic Tests")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_graph_operations,
        test_algorithms,
        test_gui_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"✗ {test.__name__} failed")
        except Exception as e:
            print(f"✗ {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"Tests completed: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! The application should work correctly.")
        print("\nTo run the application:")
        print("python main.py")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())