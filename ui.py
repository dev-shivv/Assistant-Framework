import os
import sys
import datetime
import requests
import math
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTextEdit, QHBoxLayout
from PySide6.QtCore import QTimer, Qt, QTime, QPoint
from PySide6.QtGui import QColor, QPainter, QRadialGradient, QPolygon, QPen, QBrush

class AnimatedBackgroundWidget(QWidget):
    """Custom canvas that draws smooth, lightweight floating glowing orbs."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.time_counter = 0.0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(33)  # Fires roughly every 33ms (~30 FPS)

    def update_animation(self):
        self.time_counter += 0.015
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        w, h = self.width(), self.height()
        
        # Base deep void space background
        painter.fillRect(self.rect(), QColor("#08070D"))
        
        # Orb 1: Sparkling Magenta/Pink Orb
        x1 = w * 0.35 + math.sin(self.time_counter) * (w * 0.12)
        y1 = h * 0.40 + math.cos(self.time_counter * 0.8) * (h * 0.12)
        r1 = min(w, h) * 0.45
        
        grad1 = QRadialGradient(x1, y1, r1)
        grad1.setColorAt(0, QColor(255, 0, 122, 35))
        grad1.setColorAt(0.5, QColor(255, 0, 122, 10))
        grad1.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(grad1)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(x1 - r1, y1 - r1, r1 * 2, r1 * 2)

        # Orb 2: Liquid Cyan/Blue Orb
        x2 = w * 0.65 + math.cos(self.time_counter * 1.1) * (w * 0.15)
        y2 = h * 0.60 + math.sin(self.time_counter * 0.9) * (h * 0.10)
        r2 = min(w, h) * 0.50
        
        grad2 = QRadialGradient(x2, y2, r2)
        grad2.setColorAt(0, QColor(0, 220, 255, 25))
        grad2.setColorAt(0.6, QColor(0, 220, 255, 8))
        grad2.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(grad2)
        painter.drawEllipse(x2 - r2, y2 - r2, r2 * 2, r2 * 2)


class AnalogClockWidget(QWidget):
    """A clean, glowing analog clock with its own glass backing."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(110, 110)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        w, h = self.width(), self.height()
        
        # 1. DRAW THE FROSTED GLASS BACKGROUND CIRCLE
        glass_grad = QRadialGradient(w/2, h/2, w/2)
        glass_grad.setColorAt(0, QColor(255, 255, 255, 15)) # Slight inner highlight
        glass_grad.setColorAt(1, QColor(255, 255, 255, 3))  # Fades out at edge
        
        painter.setBrush(glass_grad)
        painter.setPen(QPen(QColor(255, 255, 255, 40), 1)) # Thin specular edge border
        painter.drawEllipse(2, 2, w-4, h-4) 
        
        # 2. SETUP COORDINATES FOR THE HANDS
        painter.translate(w / 2.0, h / 2.0)
        side = min(w, h)
        painter.scale(side / 100.0, side / 100.0)

        time = QTime.currentTime()
        
        # 3. GLOWING COLORS
        hour_minute_color = QColor(0, 229, 255) # Electric Blue/Cyan
        second_color = QColor(255, 0, 122)      # Neon Pink
        tick_color = QColor(255, 255, 255, 100) # Muted White

        hour_hand = QPolygon([QPoint(2, 4), QPoint(-2, 4), QPoint(-1, -25), QPoint(1, -25)])
        minute_hand = QPolygon([QPoint(1, 4), QPoint(-1, 4), QPoint(-1, -40), QPoint(1, -40)])

        # Draw Hour Hand
        painter.save()
        painter.rotate(30.0 * (time.hour() + time.minute() / 60.0))
        painter.setPen(Qt.NoPen)
        painter.setBrush(hour_minute_color)
        painter.drawPolygon(hour_hand)
        painter.restore()

        # Draw Minute Hand
        painter.save()
        painter.rotate(6.0 * (time.minute() + time.second() / 60.0))
        painter.setPen(Qt.NoPen)
        painter.setBrush(hour_minute_color)
        painter.drawPolygon(minute_hand)
        painter.restore()

        # Draw Second Hand
        painter.save()
        painter.rotate(6.0 * time.second())
        painter.setPen(QPen(second_color, 1.5))
        painter.drawLine(0, 5, 0, -45)
        painter.setBrush(second_color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-3, -3, 6, 6) # Center pivot dot
        painter.restore()

        # Draw Tick Marks
        painter.setPen(QPen(tick_color, 1.5))
        for i in range(12):
            if i % 3 == 0:
                # Core indicators (12, 3, 6, 9) glow bright cyan
                painter.setPen(QPen(QColor(0, 229, 255, 200), 2))
                painter.drawLine(0, -48, 0, -42)
                painter.setPen(QPen(tick_color, 1.5))
            else:
                painter.drawLine(0, -48, 0, -45)
            painter.rotate(30.0)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FALCON NODE // SH1V")
        self.setObjectName("MainWindow")
        
        central_canvas = AnimatedBackgroundWidget()
        self.setCentralWidget(central_canvas)
        
        main_layout = QVBoxLayout(central_canvas)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)

        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(12)

        # LEFT COLUMN
        left_column = QVBoxLayout()
        left_column.setSpacing(12)
        
        self.client_name = QLabel("Assistant Sh1v")
        self.client_name.setObjectName("name_pannel")
        self.client_name.setAlignment(Qt.AlignCenter)
        self.client_name.setFixedHeight(45)

        self.clock_weather_card = QWidget()
        self.clock_weather_card.setObjectName("clock_weather_card")
        cw_layout = QHBoxLayout(self.clock_weather_card)
        cw_layout.setContentsMargins(12, 12, 12, 12)
        cw_layout.setSpacing(10)
        
        # New Glowing Analog Clock Instance
        self.time_label = AnalogClockWidget()
        
        self.weather_label = QLabel("Weather\nLoading...")
        self.weather_label.setObjectName("weather_text")
        self.weather_label.setAlignment(Qt.AlignCenter)
        
        cw_layout.addWidget(self.time_label, 0, Qt.AlignCenter)
        cw_layout.addWidget(self.weather_label, 1)

        self.stats_card = QWidget()
        self.stats_card.setObjectName("stats_panel")
        stats_layout = QVBoxLayout(self.stats_card)
        stats_layout.setContentsMargins(15, 12, 15, 12)
        
        self.stats_title = QLabel("SYSTEM MONITOR")
        self.stats_title.setStyleSheet("font-weight: bold; color: #FF007A; font-size: 11px; background:transparent;")
        self.stats_core = QLabel("CPU: 24%\nRAM: 3.2 GB / 8 GB\nTHREAD: ACTIVE")
        self.stats_core.setStyleSheet("font-family: 'Consolas', monospace; font-size: 11px; color: #00FFCC; background:transparent;")
        stats_layout.addWidget(self.stats_title)
        stats_layout.addWidget(self.stats_core)
        
        left_column.addWidget(self.client_name)
        left_column.addWidget(self.clock_weather_card, 2)
        left_column.addWidget(self.stats_card, 2)

        # CENTER COLUMN
        center_column = QVBoxLayout()
        center_column.setSpacing(12)
        
        self.web_search = QLineEdit()
        self.web_search.setPlaceholderText("Enter Browser Query...")
        self.web_search.setObjectName("search_bar")
        self.web_search.setFixedHeight(45)
        
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setObjectName("chat_area")
        
        center_column.addWidget(self.web_search)
        center_column.addWidget(self.chat_area)

        # RIGHT COLUMN
        right_column = QVBoxLayout()
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setPlaceholderText("System Logs...")
        self.terminal.setObjectName("terminal")
        right_column.addWidget(self.terminal)

        columns_layout.addLayout(left_column, 3)
        columns_layout.addLayout(center_column, 4)
        columns_layout.addLayout(right_column, 3)

        # BOTTOM BAR
        bottom_bar = QHBoxLayout()
        bottom_bar.setSpacing(10)
        
        self.username = QLabel("@Shivam")
        self.username.setObjectName("profile")
        self.username.setAlignment(Qt.AlignCenter)
        self.username.setFixedSize(90, 45)
        
        self.input_area = QLineEdit()
        self.input_area.setObjectName("input_area")
        self.input_area.setPlaceholderText("Input Command...")
        self.input_area.setFixedHeight(45)
        
        self.mic_button = QPushButton("🎙")
        self.mic_button.setObjectName("CircleBtn")
        self.mic_button.setFixedSize(45, 45)
        
        self.send_button = QPushButton("➤")
        self.send_button.setObjectName("CircleBtn")
        self.send_button.setFixedSize(45, 45)
        
        self.settings_button = QPushButton("⚙️")
        self.settings_button.setObjectName("CircleBtn")
        self.settings_button.setFixedSize(45, 45)

        bottom_bar.addWidget(self.username)
        bottom_bar.addWidget(self.input_area)
        bottom_bar.addWidget(self.mic_button)
        bottom_bar.addWidget(self.send_button)
        bottom_bar.addWidget(self.settings_button)

        main_layout.addLayout(columns_layout, 1)
        main_layout.addLayout(bottom_bar)
        
        try:
            self.weather_update_timer = QTimer()
            self.weather_update_timer.timeout.connect(self.update_weather)
            self.weather_update_timer.start(300000)
            self.update_weather()
        except Exception as e:
            self.log(str(e))
        
    def log_delayed(self, message, delay_ms):
        QTimer.singleShot(int(delay_ms), lambda msg=message: self.log(msg))
        
    def log(self, message):
        self.log_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.terminal.append(f">> [{self.log_time}] {message}")
        
    def get_weather(self, city="Kota"):
        api_key = "d5337f0da8f9693351084f159c03b873"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            return f"{city}\n{temp}°C\n{desc.title()}" 
        except Exception:
            return "Weather\nOffline"
    
    def update_weather(self):
        weather = self.get_weather("Kota")
        self.weather_label.setText(weather)

current_dir = os.path.dirname(os.path.abspath(__file__))
qss_path = os.path.join(current_dir, "StyleSheet.qss")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if os.path.exists(qss_path):
        with open(qss_path, "r") as file:
            app.setStyleSheet(file.read())
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())