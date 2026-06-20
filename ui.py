import os
import sys
import datetime
import time
import requests
import math
import threading
import random
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, 
    QPushButton, QLabel, QHBoxLayout, QScrollArea, QTextEdit, QStackedWidget, QSlider
)
from PySide6.QtCore import QTimer, Qt, QTime, QPoint, QPropertyAnimation, QParallelAnimationGroup, Slot, QEasingCurve, Signal
from PySide6.QtGui import QColor, QPainter, QRadialGradient, QPolygon, QPen, QFont
import engine

#self.net_btn = NetworkModeButton()
#result = engine.hey.(self.net_btn.get_state())

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
        self.theme = "dark"
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(40) 

    def update_animation(self):
        self.time_counter += 0.008 
        self.update()

    def set_theme(self, theme_name):
        self.theme = theme_name

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        
        if self.theme == "dark":
            painter.fillRect(self.rect(), QColor("#050508"))
            orb1_color = QColor(0, 229, 255, 12)
            orb2_color = QColor(140, 0, 255, 10)
        else:
            painter.fillRect(self.rect(), QColor("#F2F2F7"))
            orb1_color = QColor(0, 122, 255, 15)
            orb2_color = QColor(255, 45, 85, 12)

        x1 = w * 0.3 + math.sin(self.time_counter) * (w * 0.2)
        y1 = h * 0.4 + math.cos(self.time_counter * 0.7) * (h * 0.2)
        r1 = min(w, h) * 0.8
        grad1 = QRadialGradient(x1, y1, r1)
        grad1.setColorAt(0, orb1_color) 
        grad1.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(grad1)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(int(x1 - r1), int(y1 - r1), int(r1 * 2), int(r1 * 2))

        x2 = w * 0.7 + math.cos(self.time_counter * 0.9) * (w * 0.25)
        y2 = h * 0.6 + math.sin(self.time_counter * 0.8) * (h * 0.15)
        r2 = min(w, h) * 0.9
        grad2 = QRadialGradient(x2, y2, r2)
        grad2.setColorAt(0, orb2_color)
        grad2.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(grad2)
        painter.drawEllipse(int(x2 - r2), int(y2 - r2), int(r2 * 2), int(r2 * 2))


class AnalogClockWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(100, 100)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()

        painter.translate(w / 2.0, h / 2.0)
        side = min(w, h)
        painter.scale(side / 100.0, side / 100.0)
        time = QTime.currentTime()

        is_light = self.window().property("theme") == "light"
        hand_color = QColor(30, 30, 30, 220) if is_light else QColor(255, 255, 255, 220)
        second_color = QColor(255, 59, 48) 
        tick_color = QColor(30, 30, 30, 100) if is_light else QColor(255, 255, 255, 100)
        
        hour_hand = QPolygon([QPoint(2, 4), QPoint(-2, 4), QPoint(-1, -22), QPoint(1, -22)])
        minute_hand = QPolygon([QPoint(1, 4), QPoint(-1, 4), QPoint(-1, -38), QPoint(1, -38)])

        painter.save()
        painter.rotate(30.0 * (time.hour() + time.minute() / 60.0))
        painter.setPen(Qt.NoPen)
        painter.setBrush(hand_color)
        painter.drawPolygon(hour_hand)
        painter.restore()

        painter.save()
        painter.rotate(6.0 * (time.minute() + time.second() / 60.0))
        painter.setPen(Qt.NoPen)
        painter.setBrush(hand_color)
        painter.drawPolygon(minute_hand)
        painter.restore()

        painter.save()
        painter.rotate(6.0 * time.second())
        painter.setPen(QPen(second_color, 1.5))
        painter.drawLine(0, 5, 0, -42)
        painter.setBrush(second_color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-3, -3, 6, 6)
        painter.restore()

        for i in range(12):
            if i % 3 == 0:
                painter.setPen(QPen(hand_color, 2))
                painter.drawLine(0, -48, 0, -42)
            else:
                painter.setPen(QPen(tick_color, 1.5))
                painter.drawLine(0, -48, 0, -45)
            painter.rotate(30.0)


class HardwareMonitorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(85)
        self.target_cpu = 24
        self.target_ram = 40
        self.current_cpu = 24.0
        self.current_ram = 40.0
        
        self.logic_timer = QTimer(self)
        self.logic_timer.timeout.connect(self.simulate_load)
        self.logic_timer.start(2000)

        self.render_timer = QTimer(self)
        self.render_timer.timeout.connect(self.lerp_values)
        self.render_timer.start(30) # 30 FPS Elastic Rendering

    def simulate_load(self):
        self.target_cpu = max(5, min(95, self.target_cpu + random.randint(-20, 20)))
        self.target_ram = max(20, min(80, self.target_ram + random.randint(-8, 8)))

    def lerp_values(self):
        # Elastic interpolation: moves 10% of the distance to the target every frame
        self.current_cpu += (self.target_cpu - self.current_cpu) * 0.1
        self.current_ram += (self.target_ram - self.current_ram) * 0.1
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        is_light = self.window().property("theme") == "light"
        text_color = QColor(30, 30, 30, 200) if is_light else QColor(255, 255, 255, 200)
        value_color = QColor(10, 132, 255) if is_light else QColor(0, 229, 255)
        
        painter.setPen(text_color)
        
        # CPU Section
        painter.setFont(QFont("sans-serif", 8, QFont.Bold))
        painter.drawText(0, 15, "CPU LOAD")
        painter.setFont(QFont("Consolas", 9, QFont.Bold))
        painter.setPen(value_color)
        painter.drawText(self.width() - 40, 15, f"{int(self.current_cpu)}%")

        # RAM Section
        painter.setPen(text_color)
        painter.setFont(QFont("sans-serif", 8, QFont.Bold))
        painter.drawText(0, 50, "RAM USAGE")
        painter.setFont(QFont("Consolas", 9, QFont.Bold))
        painter.setPen(value_color)
        painter.drawText(self.width() - 50, 50, f"{int((self.current_ram/100)*8.0)} GB")

        bar_bg = QColor(0, 0, 0, 20) if is_light else QColor(255, 255, 255, 20)
        cpu_fg = QColor(10, 132, 255)
        ram_fg = QColor(191, 90, 242)

        # Thin, crisp bars
        painter.setPen(Qt.NoPen)
        painter.setBrush(bar_bg)
        painter.drawRoundedRect(0, 22, self.width(), 4, 2, 2)
        painter.setBrush(cpu_fg)
        painter.drawRoundedRect(0, 22, int((self.width()) * (self.current_cpu / 100.0)), 4, 2, 2)

        painter.setBrush(bar_bg)
        painter.drawRoundedRect(0, 57, self.width(), 4, 2, 2)
        painter.setBrush(ram_fg)
        painter.drawRoundedRect(0, 57, int((self.width()) * (self.current_ram / 100.0)), 4, 2, 2)


class MicWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(65, 65) # Container is slightly larger than the button to hold the aura
        self.is_listening = False
        self.time_step = 0.0
        
        self.btn = QPushButton("🎙", self)
        self.btn.setObjectName("mic_button")
        self.btn.setFixedSize(45, 45)
        self.btn.move(10, 10) # Center the button inside the 65x65 container
        self.btn.clicked.connect(self.toggle_listening)
        
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.update_particles)

    def toggle_listening(self):
        self.is_listening = not self.is_listening
        if self.is_listening:
            self.anim_timer.start(30)
            self.btn.setStyleSheet("color: #FF3B30; border: 1px solid rgba(255, 59, 48, 0.5);")
        else:
            self.anim_timer.stop()
            self.btn.setStyleSheet("") # Reset to QSS default
            self.update()

    def update_particles(self):
        self.time_step += 0.2
        self.update()

    def paintEvent(self, event):
        if not self.is_listening:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        center_x = self.width() / 2
        center_y = self.height() / 2
        base_radius = 26
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 59, 48, 150)) # iOS Red particles
        
        num_particles = 30
        for i in range(num_particles):
            angle = (i / num_particles) * math.pi * 2
            # Add chaotic sine waves to simulate voice frequency
            noise = math.sin(self.time_step + i) * 3 + math.cos(self.time_step * 1.5 - i) * 2
            r = base_radius + abs(noise)
            
            x = center_x + math.cos(angle) * r
            y = center_y + math.sin(angle) * r
            
            painter.drawEllipse(QPoint(int(x), int(y)), 2, 2)


class NetworkModeButton(QPushButton):
    state_change = Signal(int)
    def __init__(self):
        super().__init__()
        
        
        #self.modes = ["online", "hybrid", "offline"]
        #self.net_btn = NetworkModeButton()
        self.current_state = 0
        self.setObjectName("network_mode_btn")
        self.setFixedSize(130, 45)
        self.update_state()
        self.clicked.connect(self.cycle_mode)
        
        
    def cycle_mode(self):
        self.current_state = (self.current_state + 1) % 3 #len(self.modes)
        self.update_state()
        self.state_change.emit(self.current_state)

    def update_state(self):
        try:
            if self.current_state == 0:
                mode = str(self.current_state)
                self.setProperty("mode", mode)
                self.setText(f"NET: ONLINE")
                self.style().unpolish(self)
                self.style().polish(self)
            elif self.current_state == 1:
                mode = str(self.current_state)
                self.setProperty("mode", mode)
                self.setText(f"NET: HYBRID")
                self.style().unpolish(self)
                self.style().polish(self)
            elif self.current_state == 2:
                mode = str(self.current_state)
                self.setProperty("mode", mode)
                self.setText(f"NET: OFFLINE")
                self.style().unpolish(self)
                self.style().polish(self)
            self.get_state()
        except Exception as e:
            print(e)
            
    def get_state(self):
        return self.current_state
        #mode = self.modes[self.current_idx]
        #self.setProperty("mode", mode)
        #self.setText(f"NET: {mode.upper()}")
        #self.style().unpolish(self)
        #self.style().polish(self)


class ThinkingIndicator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(30)
        self.dot_count = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_dots)
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(12, 0, 0, 0)
        self.label = QLabel("Sh1v is thinking")
        self.label.setFont(QFont("sans-serif", 9, QFont.Medium))
        self.label.setObjectName("thinking_label")
        self.layout.addWidget(self.label)
        self.layout.addStretch()
        self.hide()

    def update_dots(self):
        self.dot_count = (self.dot_count + 1) % 4
        self.label.setText("Sh1v is processing" + "." * self.dot_count)

    def start(self):
        self.show()
        self.timer.start(400)

    def stop(self):
        self.hide()
        self.timer.stop()


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
        self.main_layout.setSpacing(4)

        self.tag_label = QLabel(self.sender_tag)
        self.tag_label.setFont(QFont("sans-serif", 8, QFont.Bold))
        self.tag_label.setObjectName("bubble_tag")

        self.bubble_body = QLabel(self.full_text if self.is_user else "")
        self.bubble_body.setWordWrap(True)
        self.bubble_body.setFont(QFont("sans-serif", 10))
        self.bubble_body.setMargin(12) 

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
        self.anim_group.setDuration(350)
        self.anim_group.setStartValue(0)
        self.anim_group.setEndValue(2000) 
        self.anim_group.setEasingCurve(QEasingCurve.OutBack) 
        self.anim_group.start()

    def stream_tokens(self, ms_interval=20):
        if self.is_user or not self.full_text:
            return
        
        main_win = self.window()
        if hasattr(main_win, 'anim_speed_slider'):
            speed_val = main_win.anim_speed_slider.value()
            ms_interval = int(ms_interval * (100 / max(1, speed_val)))

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
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        
        self.empty_label = QLabel("Assistant Sh1v Ready...")
        self.empty_label.setObjectName("empty_chat_label")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.empty_label)

        self.layout.addStretch()
        
        self.thinking_indicator = ThinkingIndicator()
        self.layout.addWidget(self.thinking_indicator)
        
        self.setWidget(self.container)
        self.is_empty = True

    def set_thinking(self, state):
        if state:
            self.thinking_indicator.start()
        else:
            self.thinking_indicator.stop()
        self._scroll_to_bottom()

    def inject_bubble(self, text, sender_tag="You", is_user=True):
        if self.is_empty:
            self.empty_label.hide()
            self.is_empty = False

        self.set_thinking(False)
        bubble = ChatBubble(text, sender_tag, is_user)
        self.layout.insertWidget(self.layout.count() - 2, bubble)
        QApplication.processEvents()

        if is_user:
            bubble.trigger_throw_animation()
        else:
            bubble.stream_tokens()
        self._scroll_to_bottom()
        return bubble

    def _scroll_to_bottom(self):
        QApplication.processEvents()
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())


class SettingsOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("settings_overlay")
        self.main_win = parent
        self.setFixedWidth(320)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(20)

        title = QLabel("System Configuration")
        title.setObjectName("settings_title")
        self.layout.addWidget(title)

        self.theme_btn = QPushButton("Switch to Light Mode")
        self.theme_btn.setObjectName("settings_btn")
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.layout.addWidget(self.theme_btn)

        self.focus_btn = QPushButton("Enable Focus Mode")
        self.focus_btn.setObjectName("settings_btn")
        self.focus_btn.clicked.connect(self.toggle_focus)
        self.layout.addWidget(self.focus_btn)

        name_lbl = QLabel("Client ID")
        self.name_input = QLineEdit()
        self.name_input.setObjectName("settings_input")
        self.name_input.setPlaceholderText("Enter username...")
        self.name_input.textChanged.connect(self.update_username)
        self.layout.addWidget(name_lbl)
        self.layout.addWidget(self.name_input)

        anim_lbl = QLabel("Animation Speed")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(50, 200)
        self.speed_slider.setValue(100)
        self.layout.addWidget(anim_lbl)
        self.layout.addWidget(self.speed_slider)
        
        self.layout.addStretch()

        close_btn = QPushButton("Close")
        close_btn.setObjectName("settings_close_btn")
        close_btn.clicked.connect(self.main_win.toggle_settings)
        self.layout.addWidget(close_btn)

    def toggle_theme(self):
        current = self.main_win.property("theme")
        new_theme = "light" if current == "dark" else "dark"
        self.main_win.setProperty("theme", new_theme)
        self.main_win.centralWidget().set_theme(new_theme)
        self.theme_btn.setText("Switch to Dark Mode" if new_theme == "light" else "Switch to Light Mode")
        self.main_win.style().unpolish(self.main_win)
        self.main_win.style().polish(self.main_win)
        self.main_win.update()

    def toggle_focus(self):
        is_focused = not self.main_win.left_panel.isVisible()
        if is_focused:
            self.main_win.left_panel.show()
            self.main_win.right_container.show()
            self.focus_btn.setText("Enable Focus Mode")
        else:
            self.main_win.left_panel.hide()
            self.main_win.right_container.hide()
            self.focus_btn.setText("Disable Focus Mode")

    def update_username(self, text):
        if text.strip():
            self.main_win.username.setText(f"@{text}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SH1V")
        self.setObjectName("MainWindow")
        self.setProperty("theme", "dark")
        self.resize(1100, 650)

        self.central_canvas = AnimatedBackgroundWidget(self)
        self.setCentralWidget(self.central_canvas)

        self.main_stack = QStackedWidget()
        canvas_layout = QVBoxLayout(self.central_canvas)
        canvas_layout.setContentsMargins(0, 0, 0, 0)
        canvas_layout.addWidget(self.main_stack)

        self.dashboard_widget = QWidget()
        main_layout = QVBoxLayout(self.dashboard_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(20)

        # ==================== LEFT COLUMN ====================
        self.left_panel = QWidget()
        left_column = QVBoxLayout(self.left_panel)
        left_column.setContentsMargins(0,0,0,0)
        left_column.setSpacing(16)

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
        
        self.hardware_monitor = HardwareMonitorWidget()
        
        stats_layout.addWidget(self.stats_title)
        stats_layout.addWidget(self.hardware_monitor)
        stats_layout.addStretch()

        left_column.addWidget(self.client_name)
        left_column.addWidget(self.clock_weather_card, 2)
        left_column.addWidget(self.stats_card, 2)

        # ==================== CENTER COLUMN ====================
        center_column = QVBoxLayout()
        center_column.setSpacing(16)

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
        self.right_outer_layout.setSpacing(12)

        self.toggle_pane_btn = QPushButton("❯")
        self.toggle_pane_btn.setFixedWidth(24)
        self.toggle_pane_btn.setObjectName("toggle_pane_btn")
        self.is_terminal_hidden = False
        self.toggle_pane_btn.clicked.connect(self.animate_edge_panel)

        self.terminal_wrapper = QWidget()
        self.terminal_wrapper.setObjectName("terminal_wrapper")
        term_layout = QVBoxLayout(self.terminal_wrapper)
        term_layout.setContentsMargins(12, 12, 12, 12)

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
        self.alt_layout.setSpacing(16)

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

        columns_layout.addWidget(self.left_panel, 3)
        columns_layout.addLayout(center_column, 4)
        columns_layout.addWidget(self.right_container, 3)

        # ==================== BOTTOM BAR ====================
        bottom_bar = QHBoxLayout()
        bottom_bar.setContentsMargins(0, 0, 0, 0)
        bottom_bar.setSpacing(12)

        self.username = QLabel("@Shivam")
        self.username.setObjectName("profile")
        self.username.setAlignment(Qt.AlignCenter)
        self.username.setFixedSize(110, 45)

        self.input_area = QLineEdit()
        self.input_area.setObjectName("input_area")
        self.input_area.setPlaceholderText("Input Command...")
        self.input_area.setFixedHeight(45)

        self.network_btn = NetworkModeButton()
        self.mic_container = MicWidget()

        self.send_button = QPushButton("➤")
        self.send_button.setObjectName("send_button")
        self.send_button.setFixedSize(45, 45)

        self.settings_button = QPushButton("⚙️")
        self.settings_button.setObjectName("settings_button")
        self.settings_button.setFixedSize(45, 45)
        self.settings_button.clicked.connect(self.toggle_settings)

        bottom_bar.addWidget(self.username)
        bottom_bar.addWidget(self.input_area)
        bottom_bar.addWidget(self.network_btn)
        bottom_bar.addWidget(self.mic_container) # Use the new Mic Container
        bottom_bar.addWidget(self.send_button)
        bottom_bar.addWidget(self.settings_button)

        main_layout.addLayout(columns_layout, 1)
        main_layout.addLayout(bottom_bar)

        self.main_stack.addWidget(self.dashboard_widget)

        # Overlay Setup
        self.settings_panel = SettingsOverlay(self)
        self.anim_speed_slider = self.settings_panel.speed_slider
        self.settings_panel.hide()
        self.settings_visible = False

        try:
            self.weather_update_timer = QTimer()
            self.weather_update_timer.timeout.connect(self.update_weather)
            self.weather_update_timer.start(300000)
            self.update_weather()
        except Exception as e:
            self.log(str(e))

        #self.send_button.clicked.connect(self._dev_test_chat)
        #self.input_area.returnPressed.connect(self._dev_test_chat)

    def toggle_settings(self):
        self.settings_panel.setGeometry(self.width(), 0, 320, self.height())
        self.settings_panel.show()
        
        self.settings_anim = QPropertyAnimation(self.settings_panel, b"geometry")
        self.settings_anim.setDuration(300)
        self.settings_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        if self.settings_visible:
            self.settings_anim.setStartValue(self.settings_panel.geometry())
            self.settings_anim.setEndValue(self.settings_panel.geometry().translated(320, 0))
            self.settings_anim.finished.connect(self.settings_panel.hide)
        else:
            self.settings_anim.setStartValue(self.settings_panel.geometry())
            self.settings_anim.setEndValue(self.settings_panel.geometry().translated(-320, 0))
            try:
                self.settings_anim.finished.disconnect()
            except:
                pass
                
        self.settings_visible = not self.settings_visible
        self.settings_anim.start()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.settings_visible:
            self.settings_panel.setGeometry(self.width() - 320, 0, 320, self.height())
        else:
            self.settings_panel.setGeometry(self.width(), 0, 320, self.height())

    def _dev_test_chat(self):
        txt = self.input_area.text()
        if txt:
            self.chat_area.inject_bubble(txt, self.username.text(), True)
            self.input_area.clear()
            self.chat_area.set_thinking(True)
            QTimer.singleShot(1000, lambda: self.chat_area.inject_bubble("Processed: " + txt, "Sh1v", False))

    def trigger_ui_utils_log(self):
        try:
            import utils_ui
            if self.main_stack.count() == 1:
                self.utils_page = utils_ui.UtilsPage(self.main_stack)
                self.main_stack.addWidget(self.utils_page)
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
