import requests
from PySide6.QtCore import QThread, Signal, Slot

class PhoneCommand(QThread):
    execution_done = Signal(dict, str)
    execution_failed = Signal(str)
    
    def __init__(self, cmd_text):
        super().__init__()
        self.cmd_text = cmd.text
        
    def run(self):
        try:
            url = "http://10.87.170.174:5005/command"
            r = requests.post(url, json={"Command": cmd_text}, timeout=5)
            
            req = r.json()
            chat = f"Okay Sir,\nYour query for \"{cmd_text}\" is completed on the target device"
            
            self.execution_done.emit(req, chat)
        except Exception as e:
            self.execution_failed.emit(str(e))
        