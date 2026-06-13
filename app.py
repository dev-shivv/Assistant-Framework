import sys
import os
import time
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
import ui
from ui import MainWindow
from engine import Parser


    
class MainApp():
    def __init__(self):
        self.interface = MainWindow()
        self.brain = Parser()
        
        self.interface.send_button.clicked.connect(self.process_command)
        self.interface.input_area.returnPressed.connect(self.process_command)
         
    def self_bubble(self, cmd_text):
        #cmd_text = self.input_area.text().strip()
        if not cmd_text:
            return
            
        self.interface.chat_area.inject_bubble(cmd_text, sender_tag="You", is_user=True)
        
    def ai_bubble(self, context):
         #self.interface.chat_area.inject_bubble(context, sender_tag="Sh1v", is_user=False)
        #self.input_area.clear()
        #self.log_delayed(f"Processing user query : {cmd_text} ",  1)
        QTimer.singleShot(600, lambda: self.interface.chat_area.inject_bubble(context, sender_tag="Sh1v", is_user=False))
    
        
    def process_command(self):
        self.command = self.interface.input_area.text()
        if not self.command.strip():
            return
        try:
            
            self.self_bubble(self.command)
            self.interface.log_delayed(f"[You] : {self.command}", 1)
            self.interface.log_delayed(f"[System] Processing...", 800)
            result = self.brain.parse(self.command)
            self.ai_bubble(result)
            self.interface.log_delayed(f" [System] Processed : {result}", 1500)
            
        except Exception as e:
            self.interface.log(f" [System] Engine Error : {str(e)}")
            
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