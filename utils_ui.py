from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class UtilsPage(QWidget):
    def __init__(self, main_stack):
        super().__init__()
        self.main_stack = main_stack
        
        # Transparent so your animated orbs still show through
        self.setStyleSheet("background: transparent;") 
        
        layout = QVBoxLayout(self)
        
        title = QLabel("FALCON UTILS ENGINE")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #00FFCC; font-size: 24px; font-weight: bold; font-family: 'monospace';")
        
        # Placeholder for your automation modules
        info = QLabel("System Automations Offline.\nDeploy automation scripts here.")
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("color: #D1F4FF; font-family: 'monospace'; font-size: 14px;")

        self.back_btn = QPushButton("❮ RETURN TO DASHBOARD")
        self.back_btn.setStyleSheet("""
            QPushButton {
                background: rgba(20, 15, 30, 160);
                color: #FF007A;
                border: 1px solid #FF007A;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 0, 122, 40);
            }
        """)
        self.back_btn.clicked.connect(self.go_back)

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(info)
        layout.addStretch()
        layout.addWidget(self.back_btn)

    def go_back(self):
        # Flips the view back to the main dashboard
        self.main_stack.setCurrentIndex(0)