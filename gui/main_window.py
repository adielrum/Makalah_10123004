#!/usr/bin/env python3
"""
Main window for vertex cover visualization tool
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter,
    QMenuBar, QMenu, QToolBar, QStatusBar, QMessageBox, QFileDialog,
    QButtonGroup, QPushButton, QLabel, QGroupBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QPixmap, QPainter
from .graph_canvas import GraphCanvas
from .algorithm_panel import AlgorithmPanel
from models import StepResult, VertexCoverResult
import json
from PyQt6.QtGui import QLinearGradient, QColor, QBrush
class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vertex Cover Visualization Tool")
        self.setGeometry(100, 100, 1200, 800)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels with a modern look
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #5A5A5A; /* Darker handle color */
                width: 2px; /* Thinner handle */
            }
        """)
        main_layout.addWidget(splitter)
        
        # Create left panel (graph canvas and tools)
        self._create_panels(splitter)
        
        # Set initial splitter proportions
        splitter.setSizes([800, 400])
        # Setup menu bar and toolbar
        self._setup_menu_bar()
        self._setup_toolbar()
        self._setup_status_bar()
        
        # Connect signals
        self._connect_signals()
        
        # Apply styling
        self._apply_styling()

    def _create_panels(self, splitter):
        """Create the left and right panels and add them to the splitter"""
        # Create left panel (graph canvas and tools)
        self.left_panel = QWidget()
        self.left_panel.setObjectName("left_panel") # Object name for styling
        left_layout = QVBoxLayout(self.left_panel)
        splitter.addWidget(self.left_panel)

        # Create right panel (algorithm controls)
        self.right_panel = QWidget()
        self.right_panel.setObjectName("right_panel") # Object name for styling
        self.algorithm_panel = AlgorithmPanel()
        right_layout = QVBoxLayout(self.right_panel)
        right_layout.addWidget(self.algorithm_panel)
        splitter.addWidget(self.right_panel)
        
        # Graph editing tools
        tools_group = QGroupBox("Graph Tools") # Simplified group box title
        tools_layout = QHBoxLayout(tools_group)
        
        # Tool buttons
        self.tool_buttons = QButtonGroup()
        
        self.add_vertex_btn = QPushButton("Add Vertex")
        self.add_vertex_btn.setCheckable(True)
        self.add_vertex_btn.setChecked(True)
        self.tool_buttons.addButton(self.add_vertex_btn, 0)
        tools_layout.addWidget(self.add_vertex_btn)
        
        self.add_edge_btn = QPushButton("Add Edge")
        self.add_edge_btn.setCheckable(True)
        self.tool_buttons.addButton(self.add_edge_btn, 1)
        tools_layout.addWidget(self.add_edge_btn)
        
        self.select_btn = QPushButton("Select/Move")
        self.select_btn.setCheckable(True)
        self.tool_buttons.addButton(self.select_btn, 2)
        tools_layout.addWidget(self.select_btn)
        
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setCheckable(True)
        self.tool_buttons.addButton(self.delete_btn, 3)
        tools_layout.addWidget(self.delete_btn)
        
        tools_layout.addStretch()
        
        self.clear_btn = QPushButton("Clear Graph")
        self.clear_btn.clicked.connect(self._clear_graph)
        tools_layout.addWidget(self.clear_btn)

        left_layout.addWidget(tools_group)
        
        # Graph canvas
        self.graph_canvas = GraphCanvas()
        left_layout.addWidget(self.graph_canvas)
        
        # Graph info
        info_layout = QHBoxLayout()
        self.graph_info_label = QLabel("Vertices: 0, Edges: 0")
        info_layout.addWidget(self.graph_info_label)
        info_layout.addStretch()
        left_layout.addLayout(info_layout)

    
    def _setup_menu_bar(self):
        """Setup the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New Graph", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self._new_graph)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open Graph", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._open_graph)
        file_menu.addAction(open_action)
        
        save_action = QAction("Save Graph", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self._save_graph)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("Export Image", self)
        export_action.triggered.connect(self._export_image)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        clear_action = QAction("Clear Graph", self)
        clear_action.triggered.connect(self._clear_graph)
        edit_menu.addAction(clear_action)
        
        clear_viz_action = QAction("Clear Visualization", self)
        clear_viz_action.triggered.connect(self._clear_visualization)
        edit_menu.addAction(clear_viz_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _setup_toolbar(self):
        """Setup the toolbar"""
        toolbar = self.addToolBar("Main")
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        
        # Add some common actions to toolbar
        new_action = QAction("New", self)
        new_action.triggered.connect(self._new_graph)
        toolbar.addAction(new_action)
        
        open_action = QAction("Open", self)
        open_action.triggered.connect(self._open_graph)
        toolbar.addAction(open_action)
        
        save_action = QAction("Save", self)
        save_action.triggered.connect(self._save_graph)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        clear_action = QAction("Clear", self)
        clear_action.triggered.connect(self._clear_graph)
        toolbar.addAction(clear_action)
    
    def _setup_status_bar(self):
        """Setup the status bar"""
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")
    
    def _connect_signals(self):
        """Connect widget signals"""
        # Tool button signals
        self.tool_buttons.buttonClicked.connect(self._on_tool_changed)
        
        # Graph canvas signals
        self.graph_canvas.graph_changed.connect(self._on_graph_changed)
        self.graph_canvas.vertex_selected.connect(self._on_vertex_selected)
        self.graph_canvas.edge_selected.connect(self._on_edge_selected)
        
        # Algorithm panel signals
        self.algorithm_panel.algorithm_step.connect(self._on_algorithm_step)
        self.algorithm_panel.algorithm_finished.connect(self._on_algorithm_finished)
    
    def _apply_styling(self):
        """Apply application styling"""
        self.setStyleSheet("""
            /* --- General Styles --- */
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                           stop:0 #1E1E2E, /* Dark base */
                                           stop:1 #282838); /* Slightly lighter */
                color: #E0E0E0; /* Light grey text */
            }
            
            /* --- Menu Bar --- */
            QMenuBar {
                background-color: #282838; /* Match window gradient start */
                color: #E0E0E0;
                border-bottom: none; /* Remove border */
            }
            QMenuBar::item {
                background-color: transparent;
                color: #E0E0E0;
                padding: 4px 10px;
            }
            QMenuBar::item:selected {
                background-color: rgba(80, 80, 100, 0.3); /* Subtle highlight */
                border-radius: 4px;
            }
            
            /* --- Menu --- */
            QMenu {
                background-color: #353545; /* Slightly darker than window */
                color: #E0E0E0;
                border: 1px solid #454555;
                border-radius: 4px;
            }
             QMenu::separator {
                height: 1px;
                background-color: #454555;
                margin-left: 10px;
                margin-right: 10px;
            }
             QMenu::item {
                padding: 5px 20px 5px 10px;
            }
            QMenu::item:selected {
                background-color: rgba(80, 80, 100, 0.5);
                 border-radius: 4px;
            }
            
            /* --- Tool Bar --- */
            QToolBar {
                background-color: #282838;
                color: #E0E0E0;
                border-bottom: none;
                spacing: 10px; /* Space between tool buttons */
            }

            /* --- Group Box --- */
            QGroupBox {
                font-weight: bold;
                color: #E0E0E0;
                border: 1px solid #454555;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
                background-color: rgba(40, 40, 50, 0.5); /* Semi-transparent background */
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #B0B0B0; /* Slightly lighter title color */
            }
            
            /* --- Labels --- */
            QLabel {
                color: #E0E0E0;
            }
            
            /* --- Buttons --- */
            QPushButton {
                background-color: #5A5A5A; /* Neutral grey button */
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                           stop:0 #6A1B9A, /* Purple start */
                                           stop:1 #AB47BC); /* Lighter purple end */
                 color: white;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QStatusBar {
                background-color: #282838;
                color: white;
                border-top: 1px solid #3A3A3A;
            }
        """)
    def _on_tool_changed(self, button):
        """Handle tool button changes"""
        tool_modes = ["add_vertex", "add_edge", "select", "delete"]
        button_id = self.tool_buttons.id(button)
        if 0 <= button_id < len(tool_modes):
            self.graph_canvas.set_mode(tool_modes[button_id])
            self.status_bar.showMessage(f"Mode: {tool_modes[button_id].replace('_', ' ').title()}")
    
    def _on_graph_changed(self):
        """Handle graph changes"""
        vertices = len(self.graph_canvas.graph.get_vertices())
        edges = len(self.graph_canvas.graph.get_edges())
        self.graph_info_label.setText(f"Vertices: {vertices}, Edges: {edges}")
        
        # Update algorithm panel
        self.algorithm_panel.set_graph(self.graph_canvas.graph)
    
    def _on_vertex_selected(self, vertex):
        """Handle vertex selection"""
        self.status_bar.showMessage(f"Selected vertex {vertex.id}")
    
    def _on_edge_selected(self, edge):
        """Handle edge selection"""
        self.status_bar.showMessage(f"Selected edge ({edge.u.id}, {edge.v.id})")
    
    def _on_algorithm_step(self, step_result: StepResult):
        """Handle algorithm step"""
        # Update visualization
        self.graph_canvas.set_vertex_cover(step_result.vertex_cover_so_far)
        
        if step_result.selected_edge:
            self.graph_canvas.set_highlighted_edges({step_result.selected_edge})
        else:
            self.graph_canvas.set_highlighted_edges(set())
        
        if step_result.removed_edges:
            self.graph_canvas.set_removed_edges(step_result.removed_edges)
        
        if step_result.added_vertices:
            self.graph_canvas.set_added_vertices(step_result.added_vertices)
        
        self.status_bar.showMessage(step_result.message)
    
    def _on_algorithm_finished(self, result: VertexCoverResult):
        """Handle algorithm completion"""
        self.graph_canvas.set_vertex_cover(result.vertex_cover)
        self.graph_canvas.set_highlighted_edges(set())
        self.graph_canvas.set_removed_edges(set())
        self.graph_canvas.set_added_vertices(set())
        
        time_taken_str = f" ({result.time_taken:.4f} seconds)" if result.time_taken is not None else ""
        self.status_bar.showMessage(f"Algorithm completed! Vertex cover size: {len(result.vertex_cover)}{time_taken_str}")
    
    def _new_graph(self):
        """Create a new graph"""
        self._clear_graph()
        self.status_bar.showMessage("New graph created")
    
    def _clear_graph(self):
        """Clear the current graph"""
        self.graph_canvas.clear_graph()
        self.status_bar.showMessage("Graph cleared")
    
    def _clear_visualization(self):
        """Clear visualization highlighting"""
        self.graph_canvas.clear_visualization_state()
        self.algorithm_panel._reset_algorithm()
        self.status_bar.showMessage("Visualization cleared")
    
    def _open_graph(self):
        """Open a graph from file"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open Graph", "", "JSON Files (*.json);;All Files (*)"
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                
                # Clear current graph
                self.graph_canvas.clear_graph()
                
                # Load vertices
                vertex_map = {}
                for v_data in data.get('vertices', []):
                    vertex = self.graph_canvas.graph.add_vertex(v_data['x'], v_data['y'])
                    vertex_map[v_data['id']] = vertex
                
                # Load edges
                for e_data in data.get('edges', []):
                    u = vertex_map.get(e_data['u'])
                    v = vertex_map.get(e_data['v'])
                    if u and v:
                        self.graph_canvas.graph.add_edge(u, v)
                
                self.graph_canvas.update()
                self._on_graph_changed()
                self.status_bar.showMessage(f"Graph loaded from {filename}")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load graph: {e}")
    
    def _save_graph(self):
        """Save the current graph to file"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Graph", "", "JSON Files (*.json);;All Files (*)"
        )
        if filename:
            try:
                # Prepare data
                vertices_data = []
                for vertex in self.graph_canvas.graph.get_vertices():
                    vertices_data.append({
                        'id': vertex.id,
                        'x': vertex.x,
                        'y': vertex.y
                    })
                
                edges_data = []
                for edge in self.graph_canvas.graph.get_edges():
                    edges_data.append({
                        'u': edge.u.id,
                        'v': edge.v.id
                    })
                
                data = {
                    'vertices': vertices_data,
                    'edges': edges_data
                }
                
                # Save to file
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
                
                self.status_bar.showMessage(f"Graph saved to {filename}")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save graph: {e}")
    
    def _export_image(self):
        """Export the graph canvas as an image"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Image", "", "PNG Files (*.png);;All Files (*)"
        )
        if filename:
            try:
                pixmap = self.graph_canvas.grab()
                pixmap.save(filename)
                self.status_bar.showMessage(f"Image exported to {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export image: {e}")
    
    def _show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About Vertex Cover Visualization Tool",
            """<h3>Vertex Cover Visualization Tool</h3>
            <p>A tool for visualizing vertex cover algorithms step by step.</p>
            <p><b>Features:</b></p>
            <ul>
            <li>Interactive graph creation and editing</li>
            <li>Step-by-step algorithm visualization</li>
            <li>Multiple vertex cover algorithms</li>
            <li>Graph import/export functionality</li>
            </ul>
            <p><b>Version:</b> 1.0</p>
            <p><b>Built with:</b> Python and PyQt6</p>
            """
        )