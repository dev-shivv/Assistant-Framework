import sys
import engine
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel

app = QApplication(sys.argv)
main_window = QMainWindow()
main_window.setWindowTitle("Assistant Sh1v")

central_canvas = QWidget()
main_window.setCentralWidget(central_canvas)

layout = QVBoxLayout(central_canvas)
    
    
input_area = QLineEdit()
input_area.setPlaceholderText("Input Your Command Here...")
    
    
result_label = QLabel(" ")

result_label.setStyleSheet("color: red;")
    
def command_handle():
    try:
        command = input_area.text()
        result_label.setText(f"Input: {command}")

        result = engine.parse(command)

        result_label.setText(result)
    except Exception as e:
        result_label.setText(str(e))
    
send_button = QPushButton("Run")
send_button.setEnabled(True)
send_button.clicked.connect(command_handle)
    
send_button.setStyleSheet("""QPushButton:pressed { background-color: red;}""")

layout.addWidget(result_label)
layout.addWidget(input_area)
layout.addWidget(send_button)


current_dir = os.path.dirname(os.path.abspath(__file__))
qss_path = os.path.join(current_dir, "style.qss")

if os.path.exists(qss_path):
    with open(qss_path, "r") as file:
        app.setStyleSheet(file.read())

main_window.show()
sys.exit(app.exec())

