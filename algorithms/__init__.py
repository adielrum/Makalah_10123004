#!/usr/bin/env python3
"""
Algorithms package for vertex cover visualization tool
"""

import importlib
import os
from typing import Dict, Any, Generator
from models import Graph, StepResult, VertexCoverResult

# Available algorithms
AVAILABLE_ALGORITHMS = {
    "2-Approximation": "two_approximation",
    "Greedy": "greedy"
}

def get_available_algorithms() -> Dict[str, str]:
    """
    Get list of available algorithms
    
    Returns:
        Dict mapping algorithm names to module names
    """
    return AVAILABLE_ALGORITHMS.copy()

def load_algorithm(algorithm_name: str):
    """
    Dynamically load an algorithm module
    
    Args:
        algorithm_name: Name of the algorithm to load
        
    Returns:
        The loaded algorithm module
        
    Raises:
        ValueError: If algorithm is not found
    """
    if algorithm_name not in AVAILABLE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algorithm_name}' not found. Available: {list(AVAILABLE_ALGORITHMS.keys())}")
    
    module_name = AVAILABLE_ALGORITHMS[algorithm_name]
    try:
        return importlib.import_module(f"algorithms.{module_name}")
    except ImportError as e:
        raise ValueError(f"Failed to load algorithm '{algorithm_name}': {e}")

def run_algorithm(algorithm_name: str, graph: Graph) -> Generator[StepResult, None, VertexCoverResult]:
    """
    Run a specific algorithm on the given graph
    
    Args:
        algorithm_name: Name of the algorithm to run
        graph: The input graph
        
    Yields:
        StepResult: Information about each step
        
    Returns:
        VertexCoverResult: Final result
    """
    algorithm_module = load_algorithm(algorithm_name)
    return algorithm_module.run(graph)

def get_algorithm_info(algorithm_name: str) -> Dict[str, Any]:
    """
    Get information about a specific algorithm
    
    Args:
        algorithm_name: Name of the algorithm
        
    Returns:
        Dictionary with algorithm information
    """
    algorithm_module = load_algorithm(algorithm_name)
    if hasattr(algorithm_module, 'get_algorithm_info'):
        return algorithm_module.get_algorithm_info()
    else:
        return {
            "name": algorithm_name,
            "description": "No description available",
            "time_complexity": "Unknown",
            "approximation_ratio": None,
            "optimal": False
        }

__all__ = ['get_available_algorithms', 'load_algorithm', 'run_algorithm', 'get_algorithm_info']