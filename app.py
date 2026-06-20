import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, QThread, Signal
import ui
from ui import MainWindow, NetworkModeButton
from engine import Parser

"""
import logging
from log_handler import handle_logs
handle_logs()
logging.basicConfig(
    filename = 'latestlog.txt',
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s'
)
logging.info("System Boot System Initialised...")
"""

class EngineWorker(QObject):
    finished = Signal(object, str)
    error = Signal(str)

    def __init__(self, command, parser):
        super().__init__()
        self.command = command
        self.parser = parser

    def run(self):
        try:
            
            output = self.parser.parse(self.command)
            
            
            if isinstance(output, tuple) and len(output) == 2:
                result, chat = output
            else:
                
                result = output
                chat = str(output) if output else "Action executed."
                
            self.finished.emit(result, chat)
        except Exception as e:
            self.error.emit(str(e))

class MainApp(QObject):
    def __init__(self):
        super().__init__()
        self.interface = MainWindow()
        self.net_button = NetworkModeButton()
        self.net_button.state_change.connect(self.state_check)
        self.brain = Parser(self.net_button)

        self.interface.send_button.clicked.connect(self.process_command)
        self.interface.input_area.returnPressed.connect(self.process_command)
        
        #self.update_state()
        #self.state = self.net_button.current_state
        #self.brain.clicked.connect(hey(self.state))
    
    def state_check(self, state):
        self.brain.set_mode(state)
    
    def self_bubble(self, cmd_text):
        if not cmd_text:
            return
        self.interface.chat_area.inject_bubble(cmd_text, sender_tag="You", is_user=True)

    def ai_bubble(self, context):
        if context:
            self.interface.chat_area.inject_bubble(context, sender_tag="Sh1v", is_user=False)

    def process_command(self):
        self.command = self.interface.input_area.text().strip()
        if not self.command:
            return

        self.self_bubble(self.command)
        self.interface.log(f"[You] : {self.command}")
        self.interface.log("[System] Processing...")
        
        self.interface.input_area.clear()
        self.interface.input_area.setEnabled(False)
        self.interface.send_button.setEnabled(False)

        self.thread = QThread()
        self.worker = EngineWorker(self.command, self.brain)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.handle_engine_success)
        self.worker.error.connect(self.handle_engine_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.error.connect(self.thread.quit)
        self.worker.error.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def handle_engine_success(self, result, chat):
        self.ai_bubble(chat)
        self.interface.log(f"[System] Processed : {result}")
        self.reset_ui()

    def handle_engine_error(self, err_msg):
        self.interface.log(f"[System] Engine Error : {err_msg}")
        self.ai_bubble("I encountered an internal system error. Check logs.")
        self.reset_ui()

    def reset_ui(self):
        self.interface.input_area.setEnabled(True)
        self.interface.send_button.setEnabled(True)
        self.interface.input_area.setFocus()
#=======================================

    def cycle_mode(self):
        self.current_state = (self.net_button.current_state + 1) % 3 #len(self.modes)
        self.net_button.update_state(self.current_state)

    



#========================================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    qss_path = os.path.join(current_dir, "StyleSheet.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r") as file:
            app.setStyleSheet(file.read())

    system = MainApp()
    system.interface.showMaximized()

    sys.exit(app.exec())