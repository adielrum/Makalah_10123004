#!/usr/bin/env python3
"""
Algorithm control panel for vertex cover visualization
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, 
    QLabel, QTextEdit, QGroupBox, QSlider, QSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from typing import Generator, Optional
from models import Graph, StepResult, VertexCoverResult
from algorithms import get_available_algorithms, run_algorithm, get_algorithm_info

class AlgorithmPanel(QWidget):
    """Control panel for algorithm selection and execution"""
    
    # Signals
    algorithm_step = pyqtSignal(StepResult)
    algorithm_finished = pyqtSignal(VertexCoverResult)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.graph = None
        self.algorithm_generator = None
        self.is_running = False
        self.current_step = 0
        self.total_steps = []
        
        # Timer for step-by-step execution
        self.step_timer = QTimer()
        self.step_timer.timeout.connect(self._execute_next_step)
        
        self._setup_ui()
        self._load_algorithms()
    
    def _setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Algorithm selection group
        algo_group = QGroupBox("Algorithm Selection")
        algo_layout = QVBoxLayout(algo_group)
        
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.currentTextChanged.connect(self._on_algorithm_changed)
        algo_layout.addWidget(QLabel("Select Algorithm:"))
        algo_layout.addWidget(self.algorithm_combo)
        
        # Algorithm info
        self.info_text = QTextEdit()
        self.info_text.setMaximumHeight(100)
        self.info_text.setReadOnly(True)
        algo_layout.addWidget(QLabel("Algorithm Information:"))
        algo_layout.addWidget(self.info_text)
        
        layout.addWidget(algo_group)
        
        # Execution controls group
        exec_group = QGroupBox("Execution Controls")
        exec_layout = QVBoxLayout(exec_group)
        
        # Speed control
        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel("Speed (ms):"))
        self.speed_spinbox = QSpinBox()
        self.speed_spinbox.setRange(100, 5000)
        self.speed_spinbox.setValue(1000)
        self.speed_spinbox.setSuffix(" ms")
        speed_layout.addWidget(self.speed_spinbox)
        exec_layout.addLayout(speed_layout)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.run_button = QPushButton("Run Algorithm")
        self.run_button.clicked.connect(self._run_algorithm)
        button_layout.addWidget(self.run_button)
        
        self.step_button = QPushButton("Next Step")
        self.step_button.clicked.connect(self._execute_next_step)
        self.step_button.setEnabled(False)
        button_layout.addWidget(self.step_button)
        
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self._pause_algorithm)
        self.pause_button.setEnabled(False)
        button_layout.addWidget(self.pause_button)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self._reset_algorithm)
        button_layout.addWidget(self.reset_button)
        
        exec_layout.addLayout(button_layout)
        
        # Progress info
        self.progress_label = QLabel("Ready to run algorithm")
        exec_layout.addWidget(self.progress_label)
        
        layout.addWidget(exec_group)
        
        # Step information group
        step_group = QGroupBox("Step Information")
        step_layout = QVBoxLayout(step_group)
        
        self.step_text = QTextEdit()
        self.step_text.setReadOnly(True)
        self.step_text.setMaximumHeight(150)
        step_layout.addWidget(self.step_text)
        
        layout.addWidget(step_group)
        
        # Results group
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout(results_group)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMaximumHeight(100)
        results_layout.addWidget(self.results_text)
        
        layout.addWidget(results_group)
        
        # Styling
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                        stop:0 #FF6A00, stop:1 #EE0979); /* Firebase-like gradient */
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 8px; /* Increased border radius for a modern look */
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                        stop:0 #EE0979, stop:1 #FF6A00); /* Reversed gradient on hover */            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QComboBox {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px;
                background: #darkgray; /* Light background */
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid; /* Visual separator */
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }

        """)
    
    def _load_algorithms(self):
        """Load available algorithms into combo box"""
        algorithms = get_available_algorithms()
        for name in algorithms.keys():
            self.algorithm_combo.addItem(name)
        
        if algorithms:
            self._on_algorithm_changed(list(algorithms.keys())[0])
    
    def _on_algorithm_changed(self, algorithm_name: str):
        """Handle algorithm selection change"""
        if algorithm_name:
            try:
                info = get_algorithm_info(algorithm_name)
                info_text = f"""<b>{info['name']}</b><br>
                <b>Description:</b> {info['description']}<br>
                <b>Time Complexity:</b> {info['time_complexity']}<br>
                <b>Approximation Ratio:</b> {info.get('approximation_ratio', 'N/A')}<br>
                <b>Optimal:</b> {'Yes' if info['optimal'] else 'No'}
                """
                self.info_text.setHtml(info_text)
            except Exception as e:
                self.info_text.setText(f"Error loading algorithm info: {e}")
    
    def set_graph(self, graph: Graph):
        """Set the graph to run algorithms on"""
        self.graph = graph
        self._reset_algorithm()
    
    def _run_algorithm(self):
        """Start running the selected algorithm"""
        if not self.graph or len(self.graph.get_edges()) == 0:
            self.step_text.setText("Please create a graph with edges first.")
            return
        
        algorithm_name = self.algorithm_combo.currentText()
        if not algorithm_name:
            return
        
        try:
            # Initialize algorithm
            self.algorithm_generator = run_algorithm(algorithm_name, self.graph)
            self.current_step = 0
            self.total_steps = []
            self.is_running = True
            
            # Update UI state
            self.run_button.setEnabled(False)
            self.step_button.setEnabled(True)
            self.pause_button.setEnabled(True)
            
            # Start automatic execution
            self.step_timer.start(self.speed_spinbox.value())
            
            self.progress_label.setText("Algorithm running...")
            self.step_text.setText("Starting algorithm execution...")
            
        except Exception as e:
            self.step_text.setText(f"Error starting algorithm: {e}")
    
    def _execute_next_step(self):
        """Execute the next step of the algorithm"""
        if not self.algorithm_generator:
            return
        
        try:
            # Get next step
            step_result = next(self.algorithm_generator)
            self.current_step += 1
            self.total_steps.append(step_result)
            
            # Update progress
            self.progress_label.setText(f"Step {self.current_step}: {step_result.message}")
            
            # Update step information
            step_info = f"""<b>Step {self.current_step}:</b><br>
            {step_result.message}<br><br>
            <b>Current Vertex Cover:</b> {[v.id for v in step_result.vertex_cover_so_far]}<br>
            <b>Remaining Edges:</b> {len(step_result.remaining_edges)}
            """
            self.step_text.setHtml(step_info)
            
            # Emit signal for visualization update
            self.algorithm_step.emit(step_result)
            
        except StopIteration as e:
            # Algorithm finished
            result = e.value
            self._algorithm_finished(result)
        except Exception as e:
            self.step_text.setText(f"Error executing step: {e}")
            self._pause_algorithm()
    
    def _algorithm_finished(self, result: VertexCoverResult):
        """Handle algorithm completion"""
        self.is_running = False
        self.step_timer.stop()
        
        # Update UI state
        self.run_button.setEnabled(True)
        self.step_button.setEnabled(False)
        self.pause_button.setEnabled(False)
        
        # Show results
        self.progress_label.setText("Algorithm completed!")
        self.results_text.setText(str(result))
        
        # Emit signal
        self.algorithm_finished.emit(result)
    
    def _pause_algorithm(self):
        """Pause algorithm execution"""
        if self.is_running:
            self.step_timer.stop()
            self.run_button.setText("Resume")
            self.run_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.progress_label.setText("Algorithm paused")
        else:
            # Resume
            self.step_timer.start(self.speed_spinbox.value())
            self.run_button.setText("Run Algorithm")
            self.run_button.setEnabled(False)
            self.pause_button.setEnabled(True)
            self.progress_label.setText("Algorithm running...")
        
        self.is_running = not self.is_running
    
    def _reset_algorithm(self):
        """Reset algorithm state"""
        self.step_timer.stop()
        self.algorithm_generator = None
        self.is_running = False
        self.current_step = 0
        self.total_steps = []
        
        # Reset UI state
        self.run_button.setText("Run Algorithm")
        self.run_button.setEnabled(True)
        self.step_button.setEnabled(False)
        self.pause_button.setEnabled(False)
        
        self.progress_label.setText("Ready to run algorithm")
        self.step_text.clear()
        self.results_text.clear()