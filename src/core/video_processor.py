#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频处理核心模块
负责视频文件的读取、帧提取、格式转换等核心功能
"""

import cv2
import numpy as np
from PIL import Image
from typing import Optional, Tuple
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QPixmap, QImage


class VideoProcessor(QObject):
    """视频处理器类"""
    
    # 信号定义
    frame_changed = Signal(QPixmap)  # 帧变化信号
    position_changed = Signal(int)   # 位置变化信号
    duration_changed = Signal(int)   # 时长变化信号
    
    def __init__(self):
        super().__init__()
        self.cap = None
        self.current_frame = None
        self.total_frames = 0
        self.fps = 0
        self.current_position = 0
        
    def load_video(self, video_path: str) -> bool:
        """
        加载视频文件
        
        Args:
            video_path: 视频文件路径
            
        Returns:
            bool: 加载成功返回True，失败返回False
        """
        try:
            if self.cap:
                self.cap.release()
                
            self.cap = cv2.VideoCapture(video_path)
            if not self.cap.isOpened():
                return False
                
            # 获取视频信息
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            
            # 发送时长信号（毫秒）
            duration_ms = int((self.total_frames / self.fps) * 1000) if self.fps > 0 else 0
            self.duration_changed.emit(duration_ms)
            
            # 读取第一帧
            self.seek_to_frame(0)
            return True
            
        except Exception as e:
            print(f"加载视频失败: {e}")
            return False
    
    def seek_to_frame(self, frame_number: int) -> bool:
        """
        跳转到指定帧
        
        Args:
            frame_number: 帧号
            
        Returns:
            bool: 跳转成功返回True
        """
        if not self.cap or frame_number < 0 or frame_number >= self.total_frames:
            return False
            
        try:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = self.cap.read()
            
            if ret:
                self.current_frame = frame
                self.current_position = frame_number
                
                # 转换为QPixmap并发送信号
                pixmap = self._cv_frame_to_pixmap(frame)
                self.frame_changed.emit(pixmap)
                self.position_changed.emit(frame_number)
                return True
                
        except Exception as e:
            print(f"跳转帧失败: {e}")
            
        return False
    
    def seek_to_time(self, time_ms: int) -> bool:
        """
        跳转到指定时间
        
        Args:
            time_ms: 时间（毫秒）
            
        Returns:
            bool: 跳转成功返回True
        """
        if not self.cap or self.fps <= 0:
            return False
            
        frame_number = int((time_ms / 1000.0) * self.fps)
        return self.seek_to_frame(frame_number)
    
    def get_current_frame_bgr(self) -> Optional[np.ndarray]:
        """
        获取当前帧的BGR格式数据
        
        Returns:
            np.ndarray: BGR格式的帧数据，失败返回None
        """
        return self.current_frame.copy() if self.current_frame is not None else None
    
    def get_current_frame_rgb(self) -> Optional[np.ndarray]:
        """
        获取当前帧的RGB格式数据
        
        Returns:
            np.ndarray: RGB格式的帧数据，失败返回None
        """
        if self.current_frame is not None:
            return cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
        return None
    
    def save_current_frame(self, output_path: str, size: Optional[Tuple[int, int]] = None) -> bool:
        """
        保存当前帧为图片
        
        Args:
            output_path: 输出文件路径
            size: 可选的输出尺寸 (width, height)
            
        Returns:
            bool: 保存成功返回True
        """
        if self.current_frame is None:
            return False
            
        try:
            # 获取RGB格式的帧
            rgb_frame = self.get_current_frame_rgb()
            if rgb_frame is None:
                return False
                
            # 转换为PIL Image
            pil_image = Image.fromarray(rgb_frame)
            
            # 如果指定了尺寸，进行缩放
            if size:
                pil_image = pil_image.resize(size, Image.Resampling.LANCZOS)
            
            # 保存图片
            pil_image.save(output_path)
            return True
            
        except Exception as e:
            print(f"保存帧失败: {e}")
            return False
    
    def get_video_info(self) -> dict:
        """
        获取视频信息
        
        Returns:
            dict: 包含视频信息的字典
        """
        if not self.cap:
            return {}
            
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        return {
            'total_frames': self.total_frames,
            'fps': self.fps,
            'width': width,
            'height': height,
            'duration_seconds': self.total_frames / self.fps if self.fps > 0 else 0
        }
    
    def _cv_frame_to_pixmap(self, cv_frame: np.ndarray) -> QPixmap:
        """
        将OpenCV帧转换为QPixmap
        
        Args:
            cv_frame: OpenCV格式的帧
            
        Returns:
            QPixmap: Qt格式的图像
        """
        rgb_frame = cv2.cvtColor(cv_frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(qt_image)
    
    def release(self):
        """释放视频资源"""
        if self.cap:
            self.cap.release()
            self.cap = None
        self.current_frame = None
        self.total_frames = 0
        self.fps = 0
        self.current_position = 0