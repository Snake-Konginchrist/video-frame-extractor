#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图像处理工具模块
提供图像格式转换、尺寸调整等工具函数
"""

import os
from typing import Tuple, List
from PIL import Image


class ImageUtils:
    """图像处理工具类"""
    
    # 支持的图像格式
    SUPPORTED_FORMATS = {
        'JPEG': ['.jpg', '.jpeg'],
        'PNG': ['.png'],
        'BMP': ['.bmp'],
        'TIFF': ['.tiff', '.tif'],
        'WEBP': ['.webp']
    }
    
    @staticmethod
    def get_supported_extensions() -> List[str]:
        """
        获取支持的图像文件扩展名列表
        
        Returns:
            List[str]: 支持的扩展名列表
        """
        extensions = []
        for format_exts in ImageUtils.SUPPORTED_FORMATS.values():
            extensions.extend(format_exts)
        return extensions
    
    @staticmethod
    def get_format_from_extension(file_path: str) -> str:
        """
        根据文件扩展名获取图像格式
        
        Args:
            file_path: 文件路径
            
        Returns:
            str: 图像格式名称
        """
        ext = os.path.splitext(file_path)[1].lower()
        
        for format_name, extensions in ImageUtils.SUPPORTED_FORMATS.items():
            if ext in extensions:
                return format_name
                
        return 'JPEG'  # 默认格式
    
    @staticmethod
    def calculate_aspect_ratio_size(original_size: Tuple[int, int], 
                                  target_width: int = None, 
                                  target_height: int = None) -> Tuple[int, int]:
        """
        根据目标宽度或高度计算保持宽高比的尺寸
        
        Args:
            original_size: 原始尺寸 (width, height)
            target_width: 目标宽度
            target_height: 目标高度
            
        Returns:
            Tuple[int, int]: 计算后的尺寸 (width, height)
        """
        orig_width, orig_height = original_size
        aspect_ratio = orig_width / orig_height
        
        if target_width and target_height:
            # 如果同时指定宽度和高度，返回指定值
            return (target_width, target_height)
        elif target_width:
            # 根据目标宽度计算高度
            new_height = int(target_width / aspect_ratio)
            return (target_width, new_height)
        elif target_height:
            # 根据目标高度计算宽度
            new_width = int(target_height * aspect_ratio)
            return (new_width, target_height)
        else:
            # 如果都没指定，返回原始尺寸
            return original_size
    
    @staticmethod
    def get_common_resolutions() -> List[Tuple[int, int]]:
        """
        获取常用分辨率列表（包含横屏和竖屏）
        
        Returns:
            List[Tuple[int, int]]: 常用分辨率列表
        """
        return [
            # 横屏分辨率
            (1920, 1080),  # Full HD 16:9
            (1280, 720),   # HD 16:9
            (1366, 768),   # WXGA 16:9
            (1024, 768),   # XGA 4:3
            (800, 600),    # SVGA 4:3
            (640, 480),    # VGA 4:3
            (3840, 2160),  # 4K UHD 16:9
            (2560, 1440),  # QHD 16:9
            (1680, 1050),  # WSXGA+ 16:10
            (1440, 900),   # WXGA+ 16:10
            (1280, 1024),  # SXGA 5:4
            (1152, 864),   # XGA+ 4:3
            
            # 竖屏分辨率
            (1080, 1920),  # 竖屏 Full HD 9:16
            (720, 1280),   # 竖屏 HD 9:16
            (768, 1366),   # 竖屏 WXGA 9:16
            (768, 1024),   # 竖屏 XGA 3:4
            (600, 800),    # 竖屏 SVGA 3:4
            (480, 640),    # 竖屏 VGA 3:4
            (2160, 3840),  # 竖屏 4K UHD 9:16
            (1440, 2560),  # 竖屏 QHD 9:16
            (1050, 1680),  # 竖屏 WSXGA+ 10:16
            (900, 1440),   # 竖屏 WXGA+ 10:16
            (1024, 1280),  # 竖屏 SXGA 4:5
            (864, 1152),   # 竖屏 XGA+ 3:4
            
            # 社交媒体常用尺寸
            (1080, 1080),  # Instagram 正方形
            (1080, 1350),  # Instagram 肖像 4:5
            (1200, 630),   # Facebook 横版 1.91:1
            (1200, 1200),  # Facebook 正方形
            (1080, 1920),  # TikTok/抖音 9:16
            (1280, 720),   # YouTube 缩略图 16:9
            (1500, 500),   # Twitter 横版 3:1
        ]
    
    @staticmethod
    def get_resolutions_by_category() -> dict:
        """
        按类别获取分辨率列表
        
        Returns:
            dict: 按类别分组的的分辨率字典
        """
        return {
            "横屏常用": [
                (1920, 1080),  # Full HD 16:9
                (1280, 720),   # HD 16:9
                (1366, 768),   # WXGA 16:9
                (1024, 768),   # XGA 4:3
                (800, 600),    # SVGA 4:3
                (640, 480),    # VGA 4:3
                (3840, 2160),  # 4K UHD 16:9
                (2560, 1440),  # QHD 16:9
            ],
            "竖屏常用": [
                (1080, 1920),  # 竖屏 Full HD 9:16
                (720, 1280),   # 竖屏 HD 9:16
                (768, 1366),   # 竖屏 WXGA 9:16
                (768, 1024),   # 竖屏 XGA 3:4
                (600, 800),    # 竖屏 SVGA 3:4
                (480, 640),    # 竖屏 VGA 3:4
                (2160, 3840),  # 竖屏 4K UHD 9:16
                (1440, 2560),  # 竖屏 QHD 9:16
            ],
            "社交媒体": [
                (1080, 1080),  # Instagram 正方形
                (1080, 1350),  # Instagram 肖像 4:5
                (1200, 630),   # Facebook 横版 1.91:1
                (1200, 1200),  # Facebook 正方形
                (1080, 1920),  # TikTok/抖音 9:16
                (1280, 720),   # YouTube 缩略图 16:9
                (1500, 500),   # Twitter 横版 3:1
            ]
        }