import sys
import os
from PySide6.QtWidgets import QApplication

import ui
from ui import MainWindow
from engine import Parser

class MainApp():
    def __init__(self):
        self.interface = MainWindow()
        self.core_logic = Parser()
        
        self.interface.send_button.clicked.connect(self.process_command)
        self.interface.input_area.returnPressed.connect(self.process_command)
        
    def process_command(self):
        self.command = self.interface.input_area.text()
        if not self.command.strip():
            return
        try:   
            result = self.core_logic.parse(self.command)
            self.interface.log(result)
            
        except Exception as e:
            self.interface.log(f"Engine Error: {str(e)}")
            
        self.interface.input_area.clear()
        
                 
if __name__ == "__main__" :
    app = QApplication(sys.argv)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    qss_path = os.path.join(current_dir, "StyleSheet.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r") as file:
            app.setStyleSheet(file.read())
            
    system = MainApp()
    system.interface.showMaximized()
    
    sys.exit(app.exec())