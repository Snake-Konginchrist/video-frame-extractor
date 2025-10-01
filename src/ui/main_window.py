#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主窗口UI模块
应用程序的主界面，整合各个组件
"""

import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QSplitter, QFrame, QFileDialog, QMessageBox)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QAction, QIcon

from ..core.video_processor import VideoProcessor
from ..utils.file_utils import FileUtils
from ..utils.image_utils import ImageUtils
from ..utils.config_utils import ConfigUtils
from .video_widget import VideoWidget
from .control_panel import ControlPanel
from .playback_controls import PlaybackControls
from ..utils.ui_utils import get_os_specific_icon_path


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.video_processor = VideoProcessor()
        self.current_video_path = None
        self.play_timer = QTimer()
        
        self.init_ui()
        self.connect_signals()
        self.setup_drag_drop()
        
    def init_ui(self):
        """初始化用户界面"""
        icon_path = get_os_specific_icon_path()
        if icon_path:
            self.setWindowIcon(QIcon(icon_path))
            
        app_name = ConfigUtils.get_app_name()
        version = ConfigUtils.get_version()
        self.setWindowTitle(f"{app_name} v{version}")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # 左侧：视频显示区域
        self.create_video_area(splitter)
        
        # 右侧：控制面板
        self.control_panel = ControlPanel()
        splitter.addWidget(self.control_panel)
        
        # 设置分割器比例
        splitter.setStretchFactor(0, 3)  # 视频区域占3/4
        splitter.setStretchFactor(1, 1)  # 控制面板占1/4
        
        # 创建菜单栏和状态栏
        self.create_menu_bar()
        self.create_status_bar()
    
    def create_video_area(self, parent):
        """创建视频显示区域"""
        video_frame = QFrame()
        video_frame.setFrameStyle(QFrame.StyledPanel)
        video_layout = QVBoxLayout(video_frame)
        
        # 视频显示控件
        self.video_widget = VideoWidget()
        video_layout.addWidget(self.video_widget)
        
        # 播放控制组件
        self.playback_controls = PlaybackControls()
        video_layout.addWidget(self.playback_controls)
        
        parent.addWidget(video_frame)
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件")
        
        open_action = QAction("打开视频", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.control_panel.on_open_clicked)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("就绪")
    
    def connect_signals(self):
        """连接信号和槽"""
        # 视频处理器信号
        self.video_processor.frame_changed.connect(self.video_widget.set_frame)
        self.video_processor.position_changed.connect(self.on_position_changed)
        self.video_processor.duration_changed.connect(self.on_duration_changed)
        
        # 控制面板信号
        self.control_panel.open_video_requested.connect(self.load_video)
        self.control_panel.frame_changed.connect(self.video_processor.seek_to_frame)
        self.control_panel.time_changed.connect(self.on_time_changed)
        self.control_panel.prev_frame_requested.connect(self.prev_frame)
        self.control_panel.next_frame_requested.connect(self.next_frame)
        self.control_panel.export_requested.connect(self.export_current_frame)
        
        # 播放控制信号
        self.playback_controls.play_pause_clicked.connect(self.toggle_play)
        self.playback_controls.progress_changed.connect(self.video_processor.seek_to_frame)
        
        # 播放定时器
        self.play_timer.timeout.connect(self.update_play_position)
        self.play_timer.setInterval(33)  # 约30fps
    
    def setup_drag_drop(self):
        """设置拖拽功能"""
        self.setAcceptDrops(True)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """拖拽进入事件"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) == 1 and FileUtils.is_video_file(urls[0].toLocalFile()):
                event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """拖拽放下事件"""
        urls = event.mimeData().urls()
        if urls:
            video_path = urls[0].toLocalFile()
            self.load_video(video_path)
    
    def load_video(self, video_path: str):
        """加载视频文件"""
        if self.video_processor.load_video(video_path):
            self.current_video_path = video_path
            
            # 更新视频信息
            info = self.video_processor.get_video_info()
            self.control_panel.update_video_info(video_path, info)
            self.playback_controls.set_duration(info['total_frames'])
            
            self.status_bar.showMessage(f"已加载视频: {os.path.basename(video_path)}")
        else:
            QMessageBox.warning(self, "错误", "无法加载视频文件")
    
    def toggle_play(self):
        """切换播放/暂停状态"""
        if not self.current_video_path:
            return
            
        is_playing = self.playback_controls.is_playing
        if is_playing:
            self.pause_video()
        else:
            self.play_video()
    
    def play_video(self):
        """播放视频"""
        self.playback_controls.set_playing_state(True)
        self.play_timer.start()
    
    def pause_video(self):
        """暂停视频"""
        self.playback_controls.set_playing_state(False)
        self.play_timer.stop()
    
    def update_play_position(self):
        """更新播放位置"""
        if not self.playback_controls.is_playing:
            return
            
        current_pos = self.video_processor.current_position
        total_frames = self.video_processor.total_frames
        
        if current_pos < total_frames - 1:
            self.video_processor.seek_to_frame(current_pos + 1)
        else:
            self.pause_video()  # 播放结束
    
    def on_position_changed(self, frame_number: int):
        """位置变化事件"""
        self.control_panel.update_position(frame_number)
        self.playback_controls.update_position(frame_number, self.video_processor.fps)
    
    def on_duration_changed(self, duration_ms: int):
        """时长变化事件"""
        pass  # 在load_video中已处理
    
    def on_time_changed(self, time_seconds: int):
        """时间变化事件"""
        if self.current_video_path:
            self.video_processor.seek_to_time(time_seconds * 1000)
    
    def prev_frame(self):
        """上一帧"""
        if not self.current_video_path:
            return
        current_pos = self.video_processor.current_position
        if current_pos > 0:
            self.video_processor.seek_to_frame(current_pos - 1)
    
    def next_frame(self):
        """下一帧"""
        if not self.current_video_path:
            return
        current_pos = self.video_processor.current_position
        total_frames = self.video_processor.total_frames
        if current_pos < total_frames - 1:
            self.video_processor.seek_to_frame(current_pos + 1)
    
    def export_current_frame(self, settings: dict):
        """导出当前帧"""
        if not self.current_video_path:
            return
        
        # 获取导出设置
        format_name = settings['format']
        output_size = settings['size']
        
        # 选择保存路径
        ext = ImageUtils.SUPPORTED_FORMATS[format_name][0]
        default_name = FileUtils.generate_output_filename(
            self.current_video_path, 
            self.video_processor.current_position,
            ext[1:]  # 移除点号
        )
        
        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setDefaultSuffix(ext[1:])
        file_dialog.selectFile(default_name)
        
        filter_str = f"{format_name} 文件 (*{ext})"
        file_dialog.setNameFilter(filter_str)
        
        if file_dialog.exec():
            output_path = file_dialog.selectedFiles()[0]
            
            # 确保目录存在
            FileUtils.ensure_directory_exists(output_path)
            
            # 保存帧
            if self.video_processor.save_current_frame(output_path, output_size):
                QMessageBox.information(self, "成功", f"帧已保存到:\n{output_path}")
                self.status_bar.showMessage(f"帧已导出: {os.path.basename(output_path)}")
            else:
                QMessageBox.warning(self, "错误", "保存帧失败")
    
    def show_about(self):
        """显示关于对话框"""
        about_text = ConfigUtils.get_about_text()
        QMessageBox.about(self, "关于", about_text)
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        self.pause_video()
        self.video_processor.release()
        event.accept()