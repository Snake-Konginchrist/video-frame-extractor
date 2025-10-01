#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频帧提取器主程序入口
"""

import sys
from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.utils.config_utils import ConfigUtils


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 从配置文件加载信息
    app.setApplicationName(ConfigUtils.get_app_name())
    app.setApplicationVersion(ConfigUtils.get_version())
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()