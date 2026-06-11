import os
import sys
import datetime
import requests
#from engine import Parser as PS
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTextEdit, QHBoxLayout
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Property, QTimer
from PySide6.QtGui import QColor, QFontDatabase

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assistant Sh1v")
        central_canvas = QWidget()
        self.setCentralWidget(central_canvas)
        layout = QVBoxLayout(central_canvas)


        self.input_area = QLineEdit()
        self.input_area.setPlaceholderText("Input Your Command Here...")
#        self.input_area.returnPressed.connect(self.command_handle)
        
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setPlaceholderText("Sh1v's' Terminal...")

        self.send_button = QPushButton("Run")
        self.send_button.setEnabled(True)
#        self.send_button.clicked.connect(self.command_handle)
        self.mic_button = QPushButton("🎙")
        self.settings_button = QPushButton("⚙️")

        self.send_button.setStyleSheet("""QPushButton:pressed { background-color: red;}""")
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        
        
        #--------—-------—
        columns = QHBoxLayout()

        left_panel = QVBoxLayout()
        self.client_name = QLabel("Assistant Sh1v")
        self.client_name.setFixedSize(225, 50)
        self.client_name.setObjectName("name_pannel")
        self.weather_label = QLabel("Weather Label Here")
        self.weather_label.setObjectName("weather_panel")
        self.time_label = QLabel(" ")
        self.time_label.setObjectName("time_panel")
        left_panel.addWidget(self.client_name)
        left_panel.addWidget(self.weather_label)
        left_panel.addWidget(self.time_label)

        center_panel = QVBoxLayout()
        self.web_search = QLineEdit()
        self.web_search.setPlaceholderText("Enter Your Browser Query Here...")
        self.web_search.setObjectName("search_bar")
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setObjectName("chat_area")
        center_panel.addWidget(self.web_search)
        center_panel.addWidget(self.chat_area)

        right_panel = QHBoxLayout()
        self.terminal.setObjectName("terminal")
        right_panel.addWidget(self.terminal)

        columns.addLayout(left_panel, 2)
        columns.addLayout(center_panel, 5)
        columns.addLayout(right_panel, 3)

        bottom_bar = QHBoxLayout()
        self.username = QLabel("@Shivam")
        self.username.setObjectName("profile")
        bottom_bar.addWidget(self.username)
        bottom_bar.addWidget(self.input_area)
        bottom_bar.addWidget(self.send_button)
        bottom_bar.addWidget(self.mic_button)
        bottom_bar.addWidget(self.settings_button)

        layout.addLayout(columns)
        layout.addLayout(bottom_bar)
        
        
        
        try:
            self.get_weather()
            self.update_weather()
            self.weather_update_timer = QTimer
            self.weather_update_timer.timeout.connect(self.update_weather)
            self.weather_update_timer.start(300000)
            
        except Exception as e:
            self.log(str(e))
        #——–----------------

    def log(self, message):
        self.terminal.append(f"》》 {message}")
        
    
    def update_time(self):
        self.current = datetime.datetime.now().strftime("%I\n%M\n%p")
        self.time_label.setText(self.current)
        
    def get_weather(self, city="Kota"):
        api_key = "d5337f0da8f9693351084f159c03b873"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"{city}\n{temp} \"C\n {desc}" 
    
    def update_weather(self):
        weather = self.get_weather("Kota")
        self.weather_label.setText(weather)
    
#    def command_handle(self):
#       try:
#            command = self.input_area.text()
            #(f"Input: {command}")
#            result = PS.parse(command)
 #           self.log(result)
  #      except Exception as e:
   #         self.log(str(e))

current_dir = os.path.dirname(os.path.abspath(__file__))
qss_path = os.path.join(current_dir, "StyleSheet.qss")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if os.path.exists(qss_path):
        with open(qss_path, "r") as file:
            app.setStyleSheet(file.read())
    main_window = MainWindow()
    # main_window.setCentralWidget(central_canvas)
    main_window.show()
    sys.exit(app.exec())