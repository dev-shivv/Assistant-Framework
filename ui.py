import os
import sys
import datetime
import time
import requests
import math
import threading
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, 
    QPushButton, QLabel, QHBoxLayout, QScrollArea, QTextEdit, QStackedWidget
)
from PySide6.QtCore import QTimer, Qt, QTime, QPoint, QPropertyAnimation, QParallelAnimationGroup, Slot, QEasingCurve, Signal
from PySide6.QtGui import QColor, QPainter, QRadialGradient, QPolygon, QPen, QFont


class ClickableBox(QWidget):
    clicked = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class AnimatedBackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.time_counter = 0.0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(33)

    def update_animation(self):
        self.time_counter += 0.015
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        painter.fillRect(self.rect(), QColor("#08070D"))
        
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
        
        glass_grad = QRadialGradient(w/2, h/2, w/2)
        glass_grad.setColorAt(0, QColor(255, 255, 255, 15))
        glass_grad.setColorAt(1, QColor(255, 255, 255, 3))
        painter.setBrush(glass_grad)
        painter.setPen(QPen(QColor(255, 255, 255, 40), 1))
        painter.drawEllipse(2, 2, w-4, h-4) 
        
        painter.translate(w / 2.0, h / 2.0)
        side = min(w, h)
        painter.scale(side / 100.0, side / 100.0)
        time = QTime.currentTime()
        
        hour_minute_color = QColor(0, 229, 255)
        second_color = QColor(255, 0, 122)
        tick_color = QColor(255, 255, 255, 100)

        hour_hand = QPolygon([QPoint(2, 4), QPoint(-2, 4), QPoint(-1, -25), QPoint(1, -25)])
        minute_hand = QPolygon([QPoint(1, 4), QPoint(-1, 4), QPoint(-1, -40), QPoint(1, -40)])

        painter.save()
        painter.rotate(30.0 * (time.hour() + time.minute() / 60.0))
        painter.setPen(Qt.NoPen)
        painter.setBrush(hour_minute_color)
        painter.drawPolygon(hour_hand)
        painter.restore()

        painter.save()
        painter.rotate(6.0 * (time.minute() + time.second() / 60.0))
        painter.setPen(Qt.NoPen)
        painter.setBrush(hour_minute_color)
        painter.drawPolygon(minute_hand)
        painter.restore()

        painter.save()
        painter.rotate(6.0 * time.second())
        painter.setPen(QPen(second_color, 1.5))
        painter.drawLine(0, 5, 0, -45)
        painter.setBrush(second_color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-3, -3, 6, 6)
        painter.restore()

        painter.setPen(QPen(tick_color, 1.5))
        for i in range(12):
            if i % 3 == 0:
                painter.setPen(QPen(QColor(0, 229, 255, 200), 2))
                painter.drawLine(0, -48, 0, -42)
                painter.setPen(QPen(tick_color, 1.5))
            else:
                painter.drawLine(0, -48, 0, -45)
            painter.rotate(30.0)


class ChatBubble(QWidget):
    def __init__(self, text, sender_tag="You", is_user=True, parent=None):
        super().__init__(parent)
        self.full_text = text
        self.sender_tag = sender_tag
        self.is_user = is_user
        self.current_frame = 0
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(4, 4, 4, 4)
        self.main_layout.setSpacing(2)

        self.tag_label = QLabel(self.sender_tag)
        self.tag_label.setFont(QFont("monospace", 9, QFont.Bold))
        
        self.bubble_body = QLabel(self.full_text if self.is_user else "")
        self.bubble_body.setWordWrap(True)
        self.bubble_body.setFont(QFont("sans-serif", 10))
        
        if self.is_user:
            self.tag_label.setObjectName("user_tag")
            self.bubble_body.setObjectName("user_bubble")
            self.tag_label.setAlignment(Qt.AlignRight)
        else:
            self.tag_label.setObjectName("ai_tag")
            self.bubble_body.setObjectName("ai_bubble")
            self.tag_label.setAlignment(Qt.AlignLeft)
        
        bubble_wrapper = QHBoxLayout()
        bubble_wrapper.setContentsMargins(0, 0, 0, 0)

        if self.is_user:
            bubble_wrapper.addStretch()
            bubble_wrapper.addWidget(self.bubble_body)
        else:
            bubble_wrapper.addWidget(self.bubble_body)
            bubble_wrapper.addStretch()

        self.main_layout.addWidget(self.tag_label)
        self.main_layout.addLayout(bubble_wrapper)

    def trigger_throw_animation(self):
        self.anim_group = QPropertyAnimation(self, b"maximumHeight")
        self.anim_group.setDuration(250)
        self.anim_group.setStartValue(0)
        self.anim_group.setEndValue(2000) 
        self.anim_group.setEasingCurve(QEasingCurve.OutQuad)
        self.anim_group.start()

    def stream_tokens(self, ms_interval=20):
        if self.is_user or not self.full_text:
            return
        self.current_frame = 0
        self.stream_timer = QTimer(self)
        self.stream_timer.timeout.connect(self._update_token)
        self.stream_timer.start(ms_interval)

    def _update_token(self):
        if self.current_frame <= len(self.full_text):
            chunk = self.full_text[:self.current_frame]
            if self.current_frame < len(self.full_text):
                chunk += " █"
            self.bubble_body.setText(chunk)
            self.current_frame += 1
            
            scroll_widget = self.window().findChild(QScrollArea, "chat_scroll_viewport")
            if scroll_widget:
                scroll_widget.verticalScrollBar().setValue(scroll_widget.verticalScrollBar().maximum())
        else:
            self.stream_timer.stop()


class ChatAreaWidget(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("chat_scroll_viewport")
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.container = QWidget()
        self.container.setObjectName("chat_container")
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(4, 4, 4, 4)
        self.layout.setSpacing(10)
        self.layout.addStretch()
        self.setWidget(self.container)

    def inject_bubble(self, text, sender_tag="You", is_user=True):
        bubble = ChatBubble(text, sender_tag, is_user)
        self.layout.insertWidget(self.layout.count() - 1, bubble)
        QApplication.processEvents()
        
        if is_user:
            bubble.trigger_throw_animation()
        else:
            bubble.stream_tokens()
        return bubble


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FALCON NODE // SH1V")
        self.setObjectName("MainWindow")
        self.resize(1000, 600)
        
        # 1. Base Canvas
        central_canvas = AnimatedBackgroundWidget()
        self.setCentralWidget(central_canvas)
        
        # 2. Stacked Engine directly on canvas
        self.main_stack = QStackedWidget()
        canvas_layout = QVBoxLayout(central_canvas)
        canvas_layout.setContentsMargins(0, 0, 0, 0)
        canvas_layout.addWidget(self.main_stack)

        # 3. Encapsulate old UI in Dashboard Container
        self.dashboard_widget = QWidget()
        self.dashboard_widget.setStyleSheet("background: transparent;")
        main_layout = QVBoxLayout(self.dashboard_widget)
        main_layout.setContentsMargins(12, 12, 12, 12)
        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(12)

        # ==================== LEFT COLUMN ====================
        left_column = QVBoxLayout()
        left_column.setSpacing(12)
        
        self.client_name = QLabel("Assistant Sh1v")
        self.client_name.setObjectName("name_pannel")
        self.client_name.setAlignment(Qt.AlignCenter)
        self.client_name.setFixedHeight(45)

        self.clock_weather_card = QWidget()
        self.clock_weather_card.setObjectName("clock_weather_card")
        cw_layout = QHBoxLayout(self.clock_weather_card)
        
        self.time_label = AnalogClockWidget()
        self.weather_label = QLabel("Weather\nLoading...")
        self.weather_label.setObjectName("weather_text")
        self.weather_label.setAlignment(Qt.AlignCenter)
        
        cw_layout.addWidget(self.time_label, 0, Qt.AlignCenter)
        cw_layout.addWidget(self.weather_label, 1)

        self.stats_card = QWidget()
        self.stats_card.setObjectName("stats_panel")
        stats_layout = QVBoxLayout(self.stats_card)
        self.stats_title = QLabel("SYSTEM MONITOR")
        self.stats_title.setObjectName("stats_title")
        self.stats_core = QLabel("CPU: 24%\nRAM: 3.2 GB / 8 GB\nTHREAD: ACTIVE")
        self.stats_core.setObjectName("stats_core")
        stats_layout.addWidget(self.stats_title)
        stats_layout.addWidget(self.stats_core)
        
        left_column.addWidget(self.client_name)
        left_column.addWidget(self.clock_weather_card, 2)
        left_column.addWidget(self.stats_card, 2)

        # ==================== CENTER COLUMN ====================
        center_column = QVBoxLayout()
        center_column.setSpacing(12)
        
        self.web_search = QLineEdit()
        self.web_search.setPlaceholderText("Enter Browser Query...")
        self.web_search.setObjectName("search_bar")
        self.web_search.setFixedHeight(45)
        
        self.chat_area = ChatAreaWidget()
        
        center_column.addWidget(self.web_search)
        center_column.addWidget(self.chat_area)

        # ==================== RIGHT COLUMN ====================
        self.right_container = QWidget()
        self.right_container.setObjectName("right_container_widget")
        self.right_outer_layout = QHBoxLayout(self.right_container)
        self.right_outer_layout.setContentsMargins(0, 0, 0, 0)
        self.right_outer_layout.setSpacing(6)

        self.toggle_pane_btn = QPushButton("❯")
        self.toggle_pane_btn.setFixedWidth(16)
        self.toggle_pane_btn.setObjectName("toggle_pane_btn")
        self.is_terminal_hidden = False
        self.toggle_pane_btn.clicked.connect(self.animate_edge_panel)

        self.terminal_wrapper = QWidget()
        self.terminal_wrapper.setObjectName("terminal_wrapper")
        term_layout = QVBoxLayout(self.terminal_wrapper)
        
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setPlaceholderText("System Logs...")
        self.terminal.setObjectName("terminal")
        term_layout.addWidget(self.terminal)

        self.alt_boxes_container = QWidget()
        self.alt_boxes_container.setObjectName("alt_boxes_container")
        self.alt_boxes_container.setMaximumWidth(0) 
        self.alt_layout = QVBoxLayout(self.alt_boxes_container)
        self.alt_layout.setContentsMargins(0, 0, 0, 0)
        self.alt_layout.setSpacing(12)

        self.box_top = ClickableBox()
        self.box_top.setObjectName("box_top_utils") 
        self.box_top.clicked.connect(self.trigger_ui_utils_log) 
        
        bt_layout = QVBoxLayout(self.box_top)
        lbl_top = QLabel("UTILS & AUTOMATION")
        lbl_top.setObjectName("box_top_title")
        lbl_top_core = QLabel("STATUS: STANDBY\nTAP TO OPEN ENGINE")
        lbl_top_core.setObjectName("box_top_core")
        bt_layout.addWidget(lbl_top)
        bt_layout.addWidget(lbl_top_core)

        self.box_bottom = QWidget()
        self.box_bottom.setObjectName("box_bottom_db")
        bb_layout = QVBoxLayout(self.box_bottom)
        lbl_bottom = QLabel("DATABASE NODES")
        lbl_bottom.setObjectName("box_bottom_title")
        lbl_bottom_core = QLabel("CLUSTER: OK\nSYNC INDEX: 99.4%\nLOG RATE: NORMAL")
        lbl_bottom_core.setObjectName("box_bottom_core")
        bb_layout.addWidget(lbl_bottom)
        bb_layout.addWidget(lbl_bottom_core)

        self.alt_layout.addWidget(self.box_top)
        self.alt_layout.addWidget(self.box_bottom)

        self.right_outer_layout.addWidget(self.toggle_pane_btn)
        self.right_outer_layout.addWidget(self.terminal_wrapper)
        self.right_outer_layout.addWidget(self.alt_boxes_container)

        columns_layout.addLayout(left_column, 3)
        columns_layout.addLayout(center_column, 4)
        columns_layout.addWidget(self.right_container, 3)

        # ==================== BOTTOM BAR ====================
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
        #self.input_area.returnPressed.connect(self.process_chat_submission)
        
        self.mic_button = QPushButton("🎙")
        self.mic_button.setObjectName("mic_button")
        self.mic_button.setFixedSize(45, 45)
        
        self.send_button = QPushButton("➤")
        self.send_button.setObjectName("send_button")
        self.send_button.setFixedSize(45, 45)
        #self.send_button.clicked.connect(self.process_chat_submission)
        
        self.settings_button = QPushButton("⚙️")
        self.settings_button.setObjectName("settings_button")
        self.settings_button.setFixedSize(45, 45)

        bottom_bar.addWidget(self.username)
        bottom_bar.addWidget(self.input_area)
        bottom_bar.addWidget(self.mic_button)
        bottom_bar.addWidget(self.send_button)
        bottom_bar.addWidget(self.settings_button)

        main_layout.addLayout(columns_layout, 1)
        main_layout.addLayout(bottom_bar)
        
        # 4. Add dashboard to stack
        self.main_stack.addWidget(self.dashboard_widget)
        
        try:
            self.weather_update_timer = QTimer()
            self.weather_update_timer.timeout.connect(self.update_weather)
            self.weather_update_timer.start(300000)
            self.update_weather()
        except Exception as e:
            self.log(str(e))

    def trigger_ui_utils_log(self):
        """Loads and switches to the Utils Page seamlessly."""
        try:
            import utils_ui
            # Only add it to the stack if it hasn't been added yet
            if self.main_stack.count() == 1:
                self.utils_page = utils_ui.UtilsPage(self.main_stack)
                self.main_stack.addWidget(self.utils_page)
            
            # Flip the card
            self.main_stack.setCurrentIndex(1)
            self.log("Switched to Utils Matrix.")
        except Exception as e:
            self.log(f"ERROR loading Utils: {e}")

    @Slot()
    def animate_edge_panel(self):
        self.terminal.hide()
        self.panel_animation = QParallelAnimationGroup(self)
        base_width = self.right_container.width()
        
        if not self.is_terminal_hidden:
            self.toggle_pane_btn.setText("❮")
            term_anim = QPropertyAnimation(self.terminal_wrapper, b"maximumWidth")
            term_anim.setDuration(300)
            term_anim.setStartValue(self.terminal_wrapper.width())
            term_anim.setEndValue(0)
            term_anim.setEasingCurve(QEasingCurve.InOutQuad)
            
            box_anim = QPropertyAnimation(self.alt_boxes_container, b"maximumWidth")
            box_anim.setDuration(300)
            box_anim.setStartValue(0)
            box_anim.setEndValue(base_width - 24)
            box_anim.setEasingCurve(QEasingCurve.OutBack)
            
            self.panel_animation.addAnimation(term_anim)
            self.panel_animation.addAnimation(box_anim)
            self.is_terminal_hidden = True
        else:
            self.toggle_pane_btn.setText("❯")
            term_anim = QPropertyAnimation(self.terminal_wrapper, b"maximumWidth")
            term_anim.setDuration(300)
            term_anim.setStartValue(0)
            term_anim.setEndValue(400) 
            term_anim.setEasingCurve(QEasingCurve.OutBack)
            
            box_anim = QPropertyAnimation(self.alt_boxes_container, b"maximumWidth")
            box_anim.setDuration(250)
            box_anim.setStartValue(self.alt_boxes_container.width())
            box_anim.setEndValue(0)
            box_anim.setEasingCurve(QEasingCurve.InOutQuad)
            
            self.panel_animation.addAnimation(term_anim)
            self.panel_animation.addAnimation(box_anim)
            self.is_terminal_hidden = False

        self.panel_animation.finished.connect(self._on_animation_finished)
        self.panel_animation.start()

    @Slot()
    def _on_animation_finished(self):
        if not self.is_terminal_hidden:
            self.terminal.show()
        
    #@Slot()
    

    def log_delayed(self, message, delay_ms):
        QTimer.singleShot(int(delay_ms), lambda msg=message: self.log(msg))
        
    def log(self, message):
        self.log_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.terminal.append(f">> [{self.log_time}] {message}")
        
    def get_weather(self, city="Kota"):
        threading.Thread(target=self._fetch_weather_thread, args=(city,), daemon=True).start()

    def _fetch_weather_thread(self, city):
        api_key = "d5337f0da8f9693351084f159c03b873"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            weather_text = f"{city}\n{temp}°C\n{desc.title()}" 
        except Exception:
            weather_text = "Weather\nOffline"
            
        QTimer.singleShot(0, lambda: self.weather_label.setText(weather_text))
    
    def update_weather(self):
        self.get_weather("Kota")

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