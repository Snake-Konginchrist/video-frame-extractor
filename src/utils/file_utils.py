#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件处理工具模块
提供文件路径处理、格式验证等工具函数
"""

import os
from typing import List


class FileUtils:
    """文件处理工具类"""
    
    # 支持的视频格式
    SUPPORTED_VIDEO_FORMATS = [
        '.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', 
        '.webm', '.m4v', '.3gp', '.ogv', '.ts', '.mts'
    ]
    
    @staticmethod
    def is_video_file(file_path: str) -> bool:
        """
        检查文件是否为支持的视频格式
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否为支持的视频格式
        """
        ext = os.path.splitext(file_path)[1].lower()
        return ext in FileUtils.SUPPORTED_VIDEO_FORMATS
    
    @staticmethod
    def get_video_files_in_directory(directory: str) -> List[str]:
        """
        获取目录中的所有视频文件
        
        Args:
            directory: 目录路径
            
        Returns:
            List[str]: 视频文件路径列表
        """
        video_files = []
        
        if not os.path.isdir(directory):
            return video_files
            
        try:
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path) and FileUtils.is_video_file(file_path):
                    video_files.append(file_path)
        except Exception as e:
            print(f"读取目录失败: {e}")
            
        return sorted(video_files)
    
    @staticmethod
    def generate_output_filename(video_path: str, frame_number: int, 
                                output_format: str = 'jpg') -> str:
        """
        生成输出文件名
        
        Args:
            video_path: 视频文件路径
            frame_number: 帧号
            output_format: 输出格式
            
        Returns:
            str: 生成的文件名
        """
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        return f"{video_name}_frame_{frame_number:06d}.{output_format}"
    
    @staticmethod
    def ensure_directory_exists(file_path: str):
        """
        确保文件所在目录存在
        
        Args:
            file_path: 文件路径
        """
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
    
    @staticmethod
    def get_safe_filename(filename: str) -> str:
        """
        获取安全的文件名（移除非法字符）
        
        Args:
            filename: 原始文件名
            
        Returns:
            str: 安全的文件名
        """
        # 移除或替换非法字符
        illegal_chars = '<>:"/\\|?*'
        safe_filename = filename
        
        for char in illegal_chars:
            safe_filename = safe_filename.replace(char, '_')
            
        return safe_filename