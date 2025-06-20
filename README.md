# Vertex Cover Visualization Tool

A comprehensive Python application for visualizing vertex cover algorithms step by step. This tool provides an interactive interface for creating graphs and running various vertex cover algorithms with real-time visualization.

## Features

### 🎨 Interactive Graph Creation
- **Add Vertices**: Click on the canvas to add new vertices
- **Create Edges**: Select two vertices to create edges between them
- **Edit/Move**: Select and drag vertices to reposition them
- **Delete**: Remove vertices or edges from the graph
- **Import/Export**: Save and load graphs in JSON format

### 🧮 Algorithm Visualization
- **Step-by-Step Execution**: Watch algorithms execute one step at a time
- **Multiple Algorithms**: Choose from different vertex cover algorithms
- **Real-Time Highlighting**: See selected edges, vertex covers, and removed edges
- **Speed Control**: Adjust the execution speed for better understanding
- **Algorithm Information**: View complexity and approximation ratios

### 📊 Available Algorithms

1. **2-Approximation Algorithm**
   - Provides a 2-approximation for minimum vertex cover
   - Time Complexity: O(E)
   - Approximation Ratio: 2.0

2. **Greedy Algorithm**
   - Selects vertices with highest degree first
   - Time Complexity: O(V × E)
   - No guaranteed approximation ratio

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download the project**:
   ```bash
   git clone <repository-url>
   cd Makalah-Stima
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## Usage Guide

### Creating a Graph

1. **Add Vertices**:
   - Select "Add Vertex" tool (default)
   - Click anywhere on the canvas to create vertices

2. **Add Edges**:
   - Select "Add Edge" tool
   - Click on the first vertex, then click on the second vertex
   - An edge will be created between them

3. **Edit Graph**:
   - Use "Select/Move" tool to drag vertices around
   - Use "Delete" tool to remove vertices or edges

### Running Algorithms

1. **Select Algorithm**:
   - Choose an algorithm from the dropdown menu
   - View algorithm information in the info panel

2. **Execute Algorithm**:
   - Click "Run Algorithm" for automatic step-by-step execution
   - Use "Next Step" for manual step-by-step execution
   - Adjust speed using the speed control

3. **View Results**:
   - Watch the visualization update in real-time
   - Read step information and final results
   - Green vertices indicate the vertex cover
   - Orange edges show currently selected edges
   - Gray dashed edges show removed edges

### File Operations

- **New Graph**: File → New Graph (Ctrl+N)
- **Open Graph**: File → Open Graph (Ctrl+O)
- **Save Graph**: File → Save Graph (Ctrl+S)
- **Export Image**: File → Export Image

## Project Structure

```
Makalah-Stima/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── models/                # Data models
│   ├── __init__.py
│   ├── graph.py           # Graph, Vertex, Edge classes
│   └── algorithm_result.py # StepResult, VertexCoverResult classes
├── algorithms/            # Algorithm implementations
│   ├── __init__.py        # Algorithm loader and manager
│   ├── two_approximation.py # 2-approximation algorithm
│   └── greedy.py          # Greedy algorithm
└── gui/                   # User interface components
    ├── __init__.py
    ├── main_window.py     # Main application window
    ├── graph_canvas.py    # Interactive graph canvas
    └── algorithm_panel.py # Algorithm control panel
```

## Adding New Algorithms

To add a new vertex cover algorithm:

1. **Create Algorithm File**:
   ```python
   # algorithms/my_algorithm.py
   from typing import Generator
   from models import Graph, StepResult, VertexCoverResult
   
   def run(graph: Graph) -> Generator[StepResult, None, VertexCoverResult]:
       # Your algorithm implementation
       pass
   
   def get_algorithm_info() -> dict:
       return {
           "name": "My Algorithm",
           "description": "Description of your algorithm",
           "time_complexity": "O(n)",
           "approximation_ratio": None,
           "optimal": False
       }
   ```

2. **Register Algorithm**:
   Add your algorithm to `AVAILABLE_ALGORITHMS` in `algorithms/__init__.py`:
   ```python
   AVAILABLE_ALGORITHMS = {
       "2-Approximation": "two_approximation",
       "Greedy": "greedy",
       "My Algorithm": "my_algorithm"  # Add this line
   }
   ```

## Algorithm Interface

All algorithms must implement the following interface:

```python
def run(graph: Graph) -> Generator[StepResult, None, VertexCoverResult]:
    """
    Run the vertex cover algorithm
    
    Args:
        graph: Input graph
        
    Yields:
        StepResult: Information about each algorithm step
        
    Returns:
        VertexCoverResult: Final algorithm result
    """
```

### StepResult Fields
- `vertex_cover_so_far`: Current vertex cover
- `remaining_edges`: Edges not yet covered
- `message`: Description of the current step
- `selected_edge`: Currently selected edge (optional)
- `added_vertices`: Vertices added in this step (optional)
- `removed_edges`: Edges removed in this step (optional)

## Technical Details

### Dependencies
- **PyQt6**: Modern GUI framework for the user interface
- **NumPy**: Numerical computations (if needed for advanced algorithms)

### Design Patterns
- **Model-View-Controller**: Separation of data, presentation, and logic
- **Observer Pattern**: Signal-slot mechanism for component communication
- **Strategy Pattern**: Pluggable algorithm system

### Performance Considerations
- Efficient graph data structures using sets for O(1) lookups
- Lazy evaluation using generators for step-by-step execution
- Optimized rendering with Qt's graphics system

## Troubleshooting

### Common Issues

1. **PyQt6 Installation Issues**:
   ```bash
   pip install --upgrade pip
   pip install PyQt6
   ```

2. **Application Won't Start**:
   - Ensure Python 3.8+ is installed
   - Check that all dependencies are installed
   - Try running with `python -m main`

3. **Graph Not Displaying**:
   - Check that vertices have been added
   - Ensure the canvas has focus
   - Try resizing the window

### Performance Tips
- For large graphs (>100 vertices), consider using manual step execution
- Reduce animation speed for better performance on slower systems
- Close other applications to free up system resources

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Code Style**: Follow PEP 8 Python style guidelines
2. **Documentation**: Add docstrings to all functions and classes
3. **Testing**: Test your changes thoroughly
4. **Algorithms**: Ensure new algorithms follow the required interface

## License

This project is created for educational purposes. Feel free to use and modify as needed.

## Acknowledgments

- Built with PyQt6 for the graphical user interface
- Inspired by classical graph theory and algorithm visualization tools
- Designed for educational use in computer science courses