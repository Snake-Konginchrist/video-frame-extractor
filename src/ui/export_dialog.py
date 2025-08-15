#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导出对话框模块
提供高级导出选项设置
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
                               QLabel, QPushButton, QComboBox, QSpinBox, 
                               QCheckBox, QGroupBox, QLineEdit, QFileDialog,
                               QMessageBox)
from PySide6.QtCore import Qt

from ..utils.image_utils import ImageUtils
from ..utils.file_utils import FileUtils


class ExportDialog(QDialog):
    """导出设置对话框类"""
    
    def __init__(self, video_info: dict, current_frame: int, parent=None):
        super().__init__(parent)
        self.video_info = video_info
        self.current_frame = current_frame
        self.output_path = ""
        
        self.init_ui()
        self.load_default_settings()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("导出设置")
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QVBoxLayout(self)
        
        # 基本设置组
        basic_group = QGroupBox("基本设置")
        basic_layout = QGridLayout(basic_group)
        
        # 输出格式
        basic_layout.addWidget(QLabel("输出格式:"), 0, 0)
        self.format_combo = QComboBox()
        self.format_combo.addItems(['JPEG', 'PNG', 'BMP', 'TIFF', 'WEBP'])
        basic_layout.addWidget(self.format_combo, 0, 1)
        
        # 输出路径
        basic_layout.addWidget(QLabel("保存路径:"), 1, 0)
        path_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)
        path_layout.addWidget(self.path_edit)
        
        self.browse_button = QPushButton("浏览...")
        self.browse_button.clicked.connect(self.browse_output_path)
        path_layout.addWidget(self.browse_button)
        
        basic_layout.addLayout(path_layout, 1, 1)
        
        layout.addWidget(basic_group)
        
        # 尺寸设置组
        size_group = QGroupBox("尺寸设置")
        size_layout = QGridLayout(size_group)
        
        # 原始尺寸显示
        size_layout.addWidget(QLabel("原始尺寸:"), 0, 0)
        original_size_text = f"{self.video_info['width']} × {self.video_info['height']}"
        size_layout.addWidget(QLabel(original_size_text), 0, 1)
        
        # 输出尺寸选项
        size_layout.addWidget(QLabel("输出尺寸:"), 1, 0)
        self.size_combo = QComboBox()
        self.size_combo.addItems(['保持原始尺寸', '自定义尺寸', '常用分辨率'])
        self.size_combo.currentTextChanged.connect(self.on_size_option_changed)
        size_layout.addWidget(self.size_combo, 1, 1)
        
        # 自定义尺寸输入
        custom_layout = QHBoxLayout()
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(1, 9999)
        self.width_spinbox.setValue(self.video_info['width'])
        self.width_spinbox.valueChanged.connect(self.on_custom_size_changed)
        custom_layout.addWidget(self.width_spinbox)
        
        custom_layout.addWidget(QLabel("×"))
        
        self.height_spinbox = QSpinBox()
        self.height_spinbox.setRange(1, 9999)
        self.height_spinbox.setValue(self.video_info['height'])
        self.height_spinbox.valueChanged.connect(self.on_custom_size_changed)
        custom_layout.addWidget(self.height_spinbox)
        
        size_layout.addLayout(custom_layout, 2, 0, 1, 2)
        
        # 分辨率类别选择
        size_layout.addWidget(QLabel("分辨率类别:"), 3, 0)
        self.category_combo = QComboBox()
        categories = ImageUtils.get_resolutions_by_category()
        self.category_combo.addItems(categories.keys())
        self.category_combo.currentTextChanged.connect(self.on_category_changed)
        size_layout.addWidget(self.category_combo, 3, 1)
        
        # 常用分辨率选择
        self.resolution_combo = QComboBox()
        self.resolution_combo.currentIndexChanged.connect(self.on_resolution_changed)
        size_layout.addWidget(self.resolution_combo, 4, 0, 1, 2)
        
        # 保持宽高比选项
        self.keep_aspect_checkbox = QCheckBox("保持宽高比")
        self.keep_aspect_checkbox.setChecked(True)
        self.keep_aspect_checkbox.toggled.connect(self.on_aspect_ratio_changed)
        size_layout.addWidget(self.keep_aspect_checkbox, 5, 0, 1, 2)
        
        layout.addWidget(size_group)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        self.export_button = QPushButton("导出")
        self.export_button.clicked.connect(self.accept_export)
        self.export_button.setDefault(True)
        button_layout.addWidget(self.export_button)
        
        layout.addLayout(button_layout)
        
        # 初始状态设置
        self.on_size_option_changed("保持原始尺寸")
        self.on_category_changed("横屏常用")
    
    def load_default_settings(self):
        """加载默认设置"""
        # 生成默认文件名
        default_name = FileUtils.generate_output_filename(
            "video", self.current_frame, "jpg"
        )
        self.path_edit.setText(default_name)
    
    def on_size_option_changed(self, option: str):
        """尺寸选项变化事件"""
        # 控制控件可用性
        is_custom = (option == "自定义尺寸")
        is_common = (option == "常用分辨率")
        
        self.width_spinbox.setEnabled(is_custom)
        self.height_spinbox.setEnabled(is_custom)
        self.category_combo.setEnabled(is_common)
        self.resolution_combo.setEnabled(is_common)
        self.keep_aspect_checkbox.setEnabled(is_custom or is_common)
        
        if option == "保持原始尺寸":
            self.width_spinbox.setValue(self.video_info['width'])
            self.height_spinbox.setValue(self.video_info['height'])
        elif option == "常用分辨率":
            # 初始化分辨率列表
            self.on_category_changed(self.category_combo.currentText())
    
    def on_custom_size_changed(self):
        """自定义尺寸变化事件"""
        if not self.keep_aspect_checkbox.isChecked():
            return
            
        sender = self.sender()
        original_size = (self.video_info['width'], self.video_info['height'])
        
        if sender == self.width_spinbox:
            # 根据宽度调整高度
            new_size = ImageUtils.calculate_aspect_ratio_size(
                original_size, target_width=self.width_spinbox.value()
            )
            self.height_spinbox.blockSignals(True)
            self.height_spinbox.setValue(new_size[1])
            self.height_spinbox.blockSignals(False)
        elif sender == self.height_spinbox:
            # 根据高度调整宽度
            new_size = ImageUtils.calculate_aspect_ratio_size(
                original_size, target_height=self.height_spinbox.value()
            )
            self.width_spinbox.blockSignals(True)
            self.width_spinbox.setValue(new_size[0])
            self.width_spinbox.blockSignals(False)
    
    def on_category_changed(self, category: str):
        """分辨率类别变化事件"""
        categories = ImageUtils.get_resolutions_by_category()
        resolutions = categories.get(category, [])
        
        self.resolution_combo.clear()
        for width, height in resolutions:
            aspect_ratio = self._get_aspect_ratio_text(width, height)
            self.resolution_combo.addItem(f"{width} × {height} ({aspect_ratio})", (width, height))
    
    def _get_aspect_ratio_text(self, width: int, height: int) -> str:
        """获取宽高比描述文本"""
        ratio = width / height
        if abs(ratio - 16/9) < 0.01:
            return "16:9"
        elif abs(ratio - 9/16) < 0.01:
            return "9:16"
        elif abs(ratio - 4/3) < 0.01:
            return "4:3"
        elif abs(ratio - 3/4) < 0.01:
            return "3:4"
        elif abs(ratio - 1) < 0.01:
            return "1:1"
        elif abs(ratio - 16/10) < 0.01:
            return "16:10"
        elif abs(ratio - 10/16) < 0.01:
            return "10:16"
        else:
            return f"{ratio:.2f}:1"

    def on_resolution_changed(self, index: int):
        """常用分辨率变化事件"""
        if index >= 0:
            width, height = self.resolution_combo.itemData(index)
            
            if self.keep_aspect_checkbox.isChecked():
                # 保持宽高比，选择合适的尺寸
                original_size = (self.video_info['width'], self.video_info['height'])
                new_size = ImageUtils.calculate_aspect_ratio_size(
                    original_size, target_width=width, target_height=height
                )
                self.width_spinbox.setValue(new_size[0])
                self.height_spinbox.setValue(new_size[1])
            else:
                self.width_spinbox.setValue(width)
                self.height_spinbox.setValue(height)
    
    def on_aspect_ratio_changed(self, checked: bool):
        """宽高比选项变化事件"""
        if checked and self.size_combo.currentText() == "自定义尺寸":
            self.on_custom_size_changed()
    
    def browse_output_path(self):
        """浏览输出路径"""
        format_name = self.format_combo.currentText()
        ext = ImageUtils.SUPPORTED_FORMATS[format_name][0]
        
        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setDefaultSuffix(ext[1:])
        
        if self.path_edit.text():
            file_dialog.selectFile(self.path_edit.text())
        
        filter_str = f"{format_name} 文件 (*{ext})"
        file_dialog.setNameFilter(filter_str)
        
        if file_dialog.exec():
            self.path_edit.setText(file_dialog.selectedFiles()[0])
    
    def accept_export(self):
        """确认导出"""
        if not self.path_edit.text().strip():
            QMessageBox.warning(self, "警告", "请选择输出路径")
            return
            
        self.output_path = self.path_edit.text()
        self.accept()
    
    def get_export_settings(self) -> dict:
        """
        获取导出设置
        
        Returns:
            dict: 导出设置字典
        """
        size_option = self.size_combo.currentText()
        output_size = None
        
        if size_option != "保持原始尺寸":
            output_size = (self.width_spinbox.value(), self.height_spinbox.value())
        
        return {
            'output_path': self.output_path,
            'format': self.format_combo.currentText(),
            'size': output_size,
            'keep_aspect_ratio': self.keep_aspect_checkbox.isChecked()
        }