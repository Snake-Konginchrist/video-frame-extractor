#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频显示控件模块
负责视频帧的显示和缩放
"""

from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter


class VideoWidget(QLabel):
    """视频显示控件类"""
    
    def __init__(self):
        super().__init__()
        self.original_pixmap = None
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                background-color: #2b2b2b;
                border: 2px solid #555555;
                border-radius: 5px;
            }
        """)
        self.setText("拖拽视频文件到此处\n或点击\"打开视频文件\"按钮")
        self.setMinimumSize(640, 360)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
    def set_frame(self, pixmap: QPixmap):
        """
        设置要显示的帧
        
        Args:
            pixmap: 要显示的QPixmap对象
        """
        self.original_pixmap = pixmap
        self.update_display()
    
    def update_display(self):
        """更新显示内容"""
        if self.original_pixmap is None:
            return
            
        # 根据控件大小缩放图像
        scaled_pixmap = self.original_pixmap.scaled(
            self.size(), 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        
        self.setPixmap(scaled_pixmap)
    
    def resizeEvent(self, event):
        """窗口大小变化事件"""
        super().resizeEvent(event)
        self.update_display()
    
    def clear_frame(self):
        """清除显示内容"""
        self.original_pixmap = None
        self.clear()
        self.setText("拖拽视频文件到此处\n或点击\"打开视频文件\"按钮")