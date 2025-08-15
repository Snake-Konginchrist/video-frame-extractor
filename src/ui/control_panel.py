#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
控制面板组件
包含文件操作、帧控制、导出设置等功能
"""

import os
from typing import Optional
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                               QLabel, QPushButton, QSpinBox, QComboBox,
                               QGroupBox, QCheckBox, QFileDialog, QMessageBox)
from PySide6.QtCore import Signal

from ..utils.file_utils import FileUtils
from ..utils.image_utils import ImageUtils


class ControlPanel(QWidget):
    """控制面板类"""
    
    # 信号定义
    open_video_requested = Signal(str)  # 请求打开视频
    frame_changed = Signal(int)  # 帧号变化
    time_changed = Signal(int)  # 时间变化
    prev_frame_requested = Signal()  # 请求上一帧
    next_frame_requested = Signal()  # 请求下一帧
    export_requested = Signal(dict)  # 请求导出
    
    def __init__(self):
        super().__init__()
        self.video_info = {}
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout(self)
        
        # 文件操作组
        self.create_file_group(layout)
        
        # 帧控制组
        self.create_frame_group(layout)
        
        # 导出设置组
        self.create_export_group(layout)
        
        # 导出按钮
        self.export_button = QPushButton("导出当前帧")
        self.export_button.setStyleSheet("QPushButton { font-weight: bold; padding: 10px; }")
        self.export_button.clicked.connect(self.on_export_clicked)
        self.export_button.setEnabled(False)
        layout.addWidget(self.export_button)
        
        # 添加弹性空间
        layout.addStretch()
    
    def create_file_group(self, parent_layout):
        """创建文件操作组"""
        file_group = QGroupBox("文件操作")
        file_layout = QVBoxLayout(file_group)
        
        self.open_button = QPushButton("打开视频文件")
        self.open_button.clicked.connect(self.on_open_clicked)
        file_layout.addWidget(self.open_button)
        
        self.video_info_label = QLabel("未加载视频")
        self.video_info_label.setWordWrap(True)
        file_layout.addWidget(self.video_info_label)
        
        parent_layout.addWidget(file_group)
    
    def create_frame_group(self, parent_layout):
        """创建帧控制组"""
        frame_group = QGroupBox("帧控制")
        frame_layout = QGridLayout(frame_group)
        
        # 当前帧显示
        frame_layout.addWidget(QLabel("当前帧:"), 0, 0)
        self.current_frame_spinbox = QSpinBox()
        self.current_frame_spinbox.setMinimum(0)
        self.current_frame_spinbox.valueChanged.connect(self.frame_changed.emit)
        frame_layout.addWidget(self.current_frame_spinbox, 0, 1)
        
        # 时间跳转
        frame_layout.addWidget(QLabel("跳转时间(秒):"), 1, 0)
        self.time_spinbox = QSpinBox()
        self.time_spinbox.setMinimum(0)
        self.time_spinbox.setSuffix(" 秒")
        self.time_spinbox.valueChanged.connect(self.time_changed.emit)
        frame_layout.addWidget(self.time_spinbox, 1, 1)
        
        # 帧导航按钮
        nav_layout = QHBoxLayout()
        self.prev_frame_button = QPushButton("上一帧")
        self.prev_frame_button.clicked.connect(self.prev_frame_requested.emit)
        nav_layout.addWidget(self.prev_frame_button)
        
        self.next_frame_button = QPushButton("下一帧")
        self.next_frame_button.clicked.connect(self.next_frame_requested.emit)
        nav_layout.addWidget(self.next_frame_button)
        
        frame_layout.addLayout(nav_layout, 2, 0, 1, 2)
        
        parent_layout.addWidget(frame_group)
    
    def create_export_group(self, parent_layout):
        """创建导出设置组"""
        export_group = QGroupBox("导出设置")
        export_layout = QGridLayout(export_group)
        
        # 输出格式
        export_layout.addWidget(QLabel("输出格式:"), 0, 0)
        self.format_combo = QComboBox()
        self.format_combo.addItems(['JPEG', 'PNG', 'BMP', 'TIFF'])
        export_layout.addWidget(self.format_combo, 0, 1)
        
        # 尺寸设置 - 直接下拉选择
        export_layout.addWidget(QLabel("输出尺寸:"), 1, 0)
        self.size_combo = QComboBox()
        self.populate_size_options()
        self.size_combo.currentTextChanged.connect(self.on_size_option_changed)
        export_layout.addWidget(self.size_combo, 1, 1)
        
        # 自定义尺寸输入（隐藏，只在选择自定义时显示）
        size_layout = QHBoxLayout()
        
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(1, 9999)
        self.width_spinbox.setValue(1920)
        self.width_spinbox.setVisible(False)
        size_layout.addWidget(self.width_spinbox)
        
        self.multiply_label = QLabel("×")
        self.multiply_label.setVisible(False)
        size_layout.addWidget(self.multiply_label)
        
        self.height_spinbox = QSpinBox()
        self.height_spinbox.setRange(1, 9999)
        self.height_spinbox.setValue(1080)
        self.height_spinbox.setVisible(False)
        size_layout.addWidget(self.height_spinbox)
        
        export_layout.addLayout(size_layout, 2, 0, 1, 2)
        
        # 保持宽高比选项
        self.keep_aspect_checkbox = QCheckBox("保持宽高比")
        self.keep_aspect_checkbox.setChecked(True)
        self.keep_aspect_checkbox.setVisible(False)
        export_layout.addWidget(self.keep_aspect_checkbox, 3, 0, 1, 2)
        
        parent_layout.addWidget(export_group)
    
    def on_open_clicked(self):
        """打开文件按钮点击事件"""
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("视频文件 (*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        
        if file_dialog.exec():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                self.open_video_requested.emit(file_paths[0])
    
    def populate_size_options(self):
        """填充尺寸选项"""
        # 原始尺寸
        self.size_combo.addItem("原始尺寸", None)
        
        # 分隔符
        self.size_combo.insertSeparator(self.size_combo.count())
        
        # 横屏常用尺寸
        self.size_combo.addItem("=== 横屏尺寸 ===", None)
        horizontal_sizes = [
            (1920, 1080, "Full HD 16:9"),
            (1280, 720, "HD 16:9"),
            (1366, 768, "WXGA 16:9"),
            (1024, 768, "XGA 4:3"),
            (3840, 2160, "4K UHD 16:9"),
            (2560, 1440, "QHD 16:9"),
        ]
        for width, height, name in horizontal_sizes:
            self.size_combo.addItem(f"{width}×{height} ({name})", (width, height))
        
        # 竖屏常用尺寸
        self.size_combo.addItem("=== 竖屏尺寸 ===", None)
        vertical_sizes = [
            (1080, 1920, "竖屏 Full HD 9:16"),
            (720, 1280, "竖屏 HD 9:16"),
            (768, 1366, "竖屏 WXGA 9:16"),
            (768, 1024, "竖屏 XGA 3:4"),
            (2160, 3840, "竖屏 4K UHD 9:16"),
            (1440, 2560, "竖屏 QHD 9:16"),
        ]
        for width, height, name in vertical_sizes:
            self.size_combo.addItem(f"{width}×{height} ({name})", (width, height))
        
        # 社交媒体尺寸
        self.size_combo.addItem("=== 社交媒体 ===", None)
        social_sizes = [
            (1080, 1080, "Instagram 正方形"),
            (1080, 1350, "Instagram 4:5"),
            (1200, 630, "Facebook 横版"),
            (1080, 1920, "TikTok/抖音"),
            (1280, 720, "YouTube 缩略图"),
        ]
        for width, height, name in social_sizes:
            self.size_combo.addItem(f"{width}×{height} ({name})", (width, height))
        
        # 分隔符
        self.size_combo.insertSeparator(self.size_combo.count())
        
        # 自定义选项
        self.size_combo.addItem("自定义尺寸...", "custom")

    def on_size_option_changed(self, option: str):
        """尺寸选项变化事件"""
        current_data = self.size_combo.currentData()
        is_custom = (current_data == "custom")
        self.width_spinbox.setVisible(is_custom)
        self.multiply_label.setVisible(is_custom)
        self.height_spinbox.setVisible(is_custom)
        self.keep_aspect_checkbox.setVisible(is_custom)
    
    def on_export_clicked(self):
        """导出按钮点击事件"""
        settings = self.get_export_settings()
        self.export_requested.emit(settings)
    
    def update_video_info(self, video_path: str, info: dict):
        """更新视频信息显示"""
        self.video_info = info
        self.export_button.setEnabled(True)
        
        info_text = f"文件: {os.path.basename(video_path)}\n"
        info_text += f"分辨率: {info['width']}×{info['height']}\n"
        info_text += f"帧率: {info['fps']:.2f} FPS\n"
        info_text += f"总帧数: {info['total_frames']}\n"
        info_text += f"时长: {info['duration_seconds']:.2f} 秒"
        self.video_info_label.setText(info_text)
        
        # 更新控件范围
        self.current_frame_spinbox.setMaximum(info['total_frames'] - 1)
        self.time_spinbox.setMaximum(int(info['duration_seconds']))
        
        # 更新自定义尺寸默认值
        self.width_spinbox.setValue(info['width'])
        self.height_spinbox.setValue(info['height'])
    
    def update_position(self, frame_number: int):
        """更新位置显示"""
        self.current_frame_spinbox.blockSignals(True)
        self.current_frame_spinbox.setValue(frame_number)
        self.current_frame_spinbox.blockSignals(False)
    
    def get_export_settings(self) -> dict:
        """获取导出设置"""
        format_name = self.format_combo.currentText()
        current_data = self.size_combo.currentData()
        
        output_size = None
        
        if current_data == "custom":
            # 自定义尺寸
            if self.keep_aspect_checkbox.isChecked():
                # 保持宽高比
                original_size = (self.video_info['width'], self.video_info['height'])
                target_width = self.width_spinbox.value()
                target_height = self.height_spinbox.value()
                
                # 根据用户输入的宽高，选择限制更严格的一个
                ratio_w = target_width / original_size[0]
                ratio_h = target_height / original_size[1]
                
                if ratio_w < ratio_h:
                    output_size = ImageUtils.calculate_aspect_ratio_size(
                        original_size, target_width=target_width)
                else:
                    output_size = ImageUtils.calculate_aspect_ratio_size(
                        original_size, target_height=target_height)
            else:
                output_size = (self.width_spinbox.value(), self.height_spinbox.value())
        elif current_data is not None:
            # 预设尺寸
            output_size = current_data
        
        return {
            'format': format_name,
            'size': output_size
        }