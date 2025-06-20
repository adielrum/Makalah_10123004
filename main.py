#!/usr/bin/env python3
"""
Vertex Cover Visualization Tool
Main application entry point
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from gui.main_window import MainWindow

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Vertex Cover Visualization Tool")
    app.setApplicationVersion("1.0")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())