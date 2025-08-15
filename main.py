#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频帧提取器主程序入口
"""

import sys
from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setApplicationName("视频帧提取器")
    app.setApplicationVersion("1.0.0")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()