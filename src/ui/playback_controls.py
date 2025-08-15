#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
播放控制组件
包含播放/暂停、进度条、时间显示等功能
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSlider, QLabel
from PySide6.QtCore import Qt, Signal


class PlaybackControls(QWidget):
    """播放控制组件类"""
    
    # 信号定义
    play_pause_clicked = Signal()  # 播放/暂停按钮点击
    progress_changed = Signal(int)  # 进度变化
    
    def __init__(self):
        super().__init__()
        self.is_playing = False
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        layout = QHBoxLayout(self)
        
        # 播放/暂停按钮
        self.play_button = QPushButton("播放")
        self.play_button.setMaximumWidth(80)
        self.play_button.clicked.connect(self.on_play_pause_clicked)
        layout.addWidget(self.play_button)
        
        # 进度滑块
        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setMinimum(0)
        self.progress_slider.valueChanged.connect(self.progress_changed.emit)
        layout.addWidget(self.progress_slider)
        
        # 时间标签
        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setMinimumWidth(100)
        layout.addWidget(self.time_label)
    
    def on_play_pause_clicked(self):
        """播放/暂停按钮点击事件"""
        self.play_pause_clicked.emit()
    
    def set_playing_state(self, is_playing: bool):
        """设置播放状态"""
        self.is_playing = is_playing
        self.play_button.setText("暂停" if is_playing else "播放")
    
    def set_duration(self, total_frames: int):
        """设置总时长"""
        self.progress_slider.setMaximum(total_frames - 1)
    
    def update_position(self, frame_number: int, fps: float):
        """更新播放位置"""
        self.progress_slider.blockSignals(True)
        self.progress_slider.setValue(frame_number)
        self.progress_slider.blockSignals(False)
        
        # 更新时间显示
        if fps > 0:
            current_time = frame_number / fps
            total_time = self.progress_slider.maximum() / fps
            
            current_str = f"{int(current_time // 60):02d}:{int(current_time % 60):02d}"
            total_str = f"{int(total_time // 60):02d}:{int(total_time % 60):02d}"
            self.time_label.setText(f"{current_str} / {total_str}")
    
    def reset(self):
        """重置控件状态"""
        self.progress_slider.setValue(0)
        self.time_label.setText("00:00 / 00:00")
        self.set_playing_state(False)