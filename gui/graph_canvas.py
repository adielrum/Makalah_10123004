#!/usr/bin/env python3
"""
Interactive graph canvas for vertex cover visualization
"""

from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, pyqtSignal, QPointF
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QMouseEvent, QPaintEvent, QLinearGradient
from typing import Optional, Set
from models import Graph, Vertex, Edge

class GraphCanvas(QWidget):
    """Interactive canvas for drawing and editing graphs"""
    
    # Signals
    graph_changed = pyqtSignal()
    vertex_selected = pyqtSignal(Vertex)
    edge_selected = pyqtSignal(Edge)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        self.setMouseTracking(True)
        
        # Graph data
        self.graph = Graph()
        
        # Visual settings
        self.vertex_radius = 25
        # Firebase-like colors
        self.vertex_color = QColor(128, 0, 128) # Purple start color for gradient
        self.vertex_hover_color = QColor(244, 180, 0) # Google Yellow
        self.vertex_selected_color = QColor(219, 68, 55) # Google Red
        self.vertex_cover_color = QColor(15, 157, 88) # Google Green
        self.vertex_gradient_color = QColor(148, 0, 211) # Darker purple end color for gradient

        self.edge_color = QColor(250, 250, 250)
        self.edge_selected_color = QColor(255, 150, 50)
        self.edge_removed_color = QColor(200, 200, 200)
        self.background_color = QColor(61, 64, 62)
        
        # Interaction state
        self.mode = "add_vertex"  # "add_vertex", "add_edge", "select", "delete"
        self.selected_vertex = None
        self.selected_edge = None
        self.edge_start_vertex = None
        self.dragging_vertex = None
        self.drag_offset = QPointF(0, 0)
        
        # Visualization state
        self.vertex_cover = set()
        self.highlighted_edges = set()
        self.removed_edges = set()
        self.added_vertices = set()
        self.hovered_vertex: Optional[Vertex] = None

        self.setStyleSheet("""
            GraphCanvas {
                background-color: #3d403e;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
    
    def set_mode(self, mode: str):
        """Set interaction mode"""
        self.mode = mode
        self.selected_vertex = None
        self.selected_edge = None
        self.edge_start_vertex = None
        self.update()
    
    def clear_graph(self):
        """Clear the graph"""
        self.graph.clear()
        self.clear_visualization_state()
        self.graph_changed.emit()
        self.update()
    
    def clear_visualization_state(self):
        """Clear visualization highlighting"""
        self.vertex_cover.clear()
        self.highlighted_edges.clear()
        self.removed_edges.clear()
        self.added_vertices.clear()
        self.selected_vertex = None
        self.selected_edge = None
        self.update()
    
    def set_vertex_cover(self, vertex_cover: Set[Vertex]):
        """Set vertices to highlight as part of vertex cover"""
        self.vertex_cover = vertex_cover.copy()
        self.update()
    
    def set_highlighted_edges(self, edges: Set[Edge]):
        """Set edges to highlight"""
        self.highlighted_edges = edges.copy()
        self.update()
    
    def set_removed_edges(self, edges: Set[Edge]):
        """Set edges to show as removed"""
        self.removed_edges = edges.copy()
        self.update()
    
    def set_added_vertices(self, vertices: Set[Vertex]):
        """Set vertices to highlight as newly added"""
        self.added_vertices = vertices.copy()
        self.update()
    
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press events"""
        pos = event.position()
        x, y = pos.x(), pos.y()
        
        # Find vertex at click position
        clicked_vertex = self.graph.get_vertex_at_position(x, y, self.vertex_radius)
        
        if event.button() == Qt.MouseButton.LeftButton:
            if self.mode == "add_vertex":
                if not clicked_vertex:
                    # Add new vertex
                    vertex = self.graph.add_vertex(x, y)
                    self.graph_changed.emit()
                    self.update()
            
            elif self.mode == "add_edge":
                if clicked_vertex:
                    if self.edge_start_vertex is None:
                        # Start edge creation
                        self.edge_start_vertex = clicked_vertex
                        self.selected_vertex = clicked_vertex
                        self.hovered_vertex = None # Clear hover
                    else:
                        # Complete edge creation
                        if clicked_vertex != self.edge_start_vertex:
                            success = self.graph.add_edge(self.edge_start_vertex, clicked_vertex)
                            if success:
                                self.graph_changed.emit()
                        self.edge_start_vertex = None
                        self.selected_vertex = None
                        self.hovered_vertex = None # Clear hover
                    self.update()
            
            elif self.mode == "select":
                if clicked_vertex:
                    self.selected_vertex = clicked_vertex
                    self.selected_edge = None
                    self.vertex_selected.emit(clicked_vertex)
                    # Start dragging
                    self.dragging_vertex = clicked_vertex
                    self.drag_offset = QPointF(x - clicked_vertex.x, y - clicked_vertex.y)
                else:
                    # Check if clicked on edge
                    self.dragging_vertex = None # Ensure dragging is off if clicking background
                    clicked_edge = self._find_edge_at_position(x, y)
                    if clicked_edge:
                        self.selected_edge = clicked_edge
                        self.selected_vertex = None
                        self.edge_selected.emit(clicked_edge)
                    else:
                        self.selected_vertex = None
                        self.selected_edge = None
                self.hovered_vertex = None # Clear hover on click
                self.update()
            
            elif self.mode == "delete":
                if clicked_vertex:
                    self.graph.remove_vertex(clicked_vertex)
                    self.graph_changed.emit()
                    self.update()
                else:
                    # Check if clicked on edge
                    clicked_edge = self._find_edge_at_position(x, y)
                    if clicked_edge:
                        self.graph.remove_edge(clicked_edge)
                        self.graph_changed.emit()
                self.hovered_vertex = None # Clear hover on click
                self.update()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle mouse move events"""
        if self.dragging_vertex and self.mode == "select":
            pos = event.position()
            new_x = pos.x() - self.drag_offset.x()
            new_y = pos.y() - self.drag_offset.y()
            
            # Update vertex position
            # Since Vertex is immutable, we need to recreate it
            old_vertex = self.dragging_vertex
            new_vertex = Vertex(old_vertex.id, new_x, new_y)
            
            # Update graph
            self.graph._vertices.remove(old_vertex)
            self.graph._vertices.add(new_vertex)
            
            # Update edges
            edges_to_update = []
            for edge in self.graph._edges:
                if edge.u == old_vertex or edge.v == old_vertex:
                    edges_to_update.append(edge)
            
            for edge in edges_to_update:
                self.graph._edges.remove(edge)
                new_u = new_vertex if edge.u == old_vertex else edge.u
                new_v = new_vertex if edge.v == old_vertex else edge.v
                self.graph._edges.add(Edge(new_u, new_v))
            
            # Update references
            self.dragging_vertex = new_vertex
            if self.selected_vertex == old_vertex:
                self.selected_vertex = new_vertex
            
            self.hovered_vertex = None # Clear hover while dragging
            self.update()
        elif self.mode != "delete": # Don't highlight vertex on hover in delete mode
            # Update hovered vertex for visual feedback
            pos = event.position()
            x, y = pos.x(), pos.y()
            hovered = self.graph.get_vertex_at_position(x, y, self.vertex_radius)
            if hovered != self.hovered_vertex:
                self.hovered_vertex = hovered
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release events"""
        if self.dragging_vertex:
            self.dragging_vertex = None
            self.graph_changed.emit()
    
    def _find_edge_at_position(self, x: float, y: float, tolerance: float = 5.0) -> Optional[Edge]:
        """Find edge near the given position"""
        for edge in self.graph.get_edges():
            # Calculate distance from point to line segment
            x1, y1 = edge.u.x, edge.u.y
            x2, y2 = edge.v.x, edge.v.y
            
            # Vector from start to end
            dx = x2 - x1
            dy = y2 - y1
            
            if dx == 0 and dy == 0:
                # Degenerate case
                distance = ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5
            else:
                # Parameter t for closest point on line
                t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)))
                
                # Closest point on line segment
                closest_x = x1 + t * dx
                closest_y = y1 + t * dy
                
                # Distance to closest point
                distance = ((x - closest_x) ** 2 + (y - closest_y) ** 2) ** 0.5
            
            if distance <= tolerance:
                return edge
        
        return None
    
    def paintEvent(self, event: QPaintEvent):
        """Paint the graph"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw background gradient
        # Using a subtle linear gradient for a modern look
        gradient = QColor(61, 64, 62)
        painter.fillRect(self.rect(), gradient)

        # Original fill for compatibility, can be removed if gradient is preferred
        painter.fillRect(self.rect(), self.background_color)
        
        # Draw edges
        self._draw_edges(painter)
        
        # Draw vertices
        self._draw_vertices(painter)
        
        # Draw edge being created
        if self.mode == "add_edge" and self.edge_start_vertex:
            self._draw_edge_preview(painter)
    
    def _draw_edges(self, painter: QPainter):
        """Draw all edges"""
        for edge in self.graph.get_edges():
            # Determine edge color and style
            if edge in self.removed_edges:
                pen = QPen(self.edge_removed_color, 2, Qt.PenStyle.DashLine)
            elif edge in self.highlighted_edges:
                pen = QPen(self.edge_selected_color, 3, Qt.PenStyle.SolidLine)
            elif edge == self.selected_edge:
                 pen = QPen(self.edge_selected_color, 3, Qt.PenStyle.DotLine) # Different style for selected edge
            else:
                pen = QPen(self.edge_color, 2)
            
            painter.setPen(pen)
            painter.drawLine(int(edge.u.x), int(edge.u.y), int(edge.v.x), int(edge.v.y))

    
    def _draw_vertices(self, painter: QPainter):
        """Draw all vertices"""
        font = QFont("Arial", 12, QFont.Weight.Bold)
        painter.setFont(font)
        
        for vertex in self.graph.get_vertices():
            # Determine vertex color and brush
            if vertex == self.selected_vertex:
                brush = QBrush(self.vertex_selected_color)
            elif vertex == self.hovered_vertex:
                brush = QBrush(self.vertex_hover_color)
            elif vertex in self.vertex_cover:
                brush = QBrush(self.vertex_cover_color)
            elif vertex in self.added_vertices:
                brush = QBrush(self.vertex_selected_color) # Highlight newly added vertices
            else:
                # Apply gradient for default vertices
                gradient = QLinearGradient(vertex.x - self.vertex_radius, vertex.y - self.vertex_radius,
                                           vertex.x + self.vertex_radius, vertex.y + self.vertex_radius)
                gradient.setColorAt(0, self.vertex_color)
                gradient.setColorAt(1, self.vertex_gradient_color)
                brush = QBrush(gradient)
            
            # Draw vertex circle
            painter.setPen(QPen(Qt.GlobalColor.transparent, 0)) # Remove outline
            painter.setBrush(brush)
            painter.drawEllipse(
                int(vertex.x - self.vertex_radius),
                int(vertex.y - self.vertex_radius),
                self.vertex_radius * 2,
                self.vertex_radius * 2
            )
            
            # Draw vertex ID
            painter.setPen(QPen(Qt.GlobalColor.white)) # Change text color to white
            painter.drawText(
                int(vertex.x - 10),
                int(vertex.y + 5),
                str(vertex.id)
            )
    
    def _draw_edge_preview(self, painter: QPainter):
        """Draw edge being created"""
        if self.edge_start_vertex:
            painter.setPen(QPen(self.edge_selected_color, 2, Qt.PenStyle.DashLine))
            mouse_pos = self.mapFromGlobal(self.cursor().pos())
            painter.drawLine(
                int(self.edge_start_vertex.x),
                int(self.edge_start_vertex.y),
                int(mouse_pos.x()),
                int(mouse_pos.y())
            )