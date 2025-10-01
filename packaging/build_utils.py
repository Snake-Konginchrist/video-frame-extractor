"""
构建工具模块。

该模块提供运行构建过程的核心功能，
包括执行 shell 命令和构建 PyInstaller 命令。
"""

import subprocess
import sys
from packaging import build_config

def run_command(command):
    """执行一个 shell 命令并实时打印其输出。"""
    print(f"\n-- 正在执行命令: {' '.join(command)}\n")
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip(), flush=True)

        return_code = process.poll()
        if return_code != 0:
            print(f"\n-- 命令执行失败，退出代码: {return_code}")
            return False
        print("\n-- 命令执行成功。")
        return True

    except FileNotFoundError:
        print(f"\n-- 错误: 命令 '{command[0]}' 未找到。")
        print("-- 请确保已安装 PyInstaller ('pip install pyinstaller')。")
        return False
    except Exception as e:
        print(f"\n-- 发生意外错误: {e}")
        return False

def build_with_pyinstaller(target_os, arch, mode):
    """根据用户选择构建并执行 PyInstaller 命令。"""
    print(f"\n-- 开始为 {target_os.capitalize()} ({arch}) 进行构建 --")

    # 确保构建依赖已安装 (包括 toml 用于解析配置文件)
    # 已根据您的 pyproject.toml 更正为 pyside6
    print("\n-- 正在检查并安装所需依赖 (pyinstaller, pyside6, toml)...")
    if not run_command([sys.executable, "-m", "pip", "install", "pyinstaller", "pyside6", "toml"]):
        print("\n-- 安装构建依赖失败。正在中止。")
        return

    command = [
        "pyinstaller",
        build_config.MAIN_SCRIPT,
        "--name", build_config.APP_NAME,
        "--windowed",  # 对 GUI 应用很重要
        "--clean",     # 清理 PyInstaller 缓存并删除临时文件
        build_config.BUILD_MODES[mode]["flag"],
    ]

    # 添加特定于操作系统的选项
    if target_os in build_config.SUPPORTED_PLATFORMS:
        # 注意：您需要创建图标文件才能使此功能生效。
        # icon_path = build_config.SUPPORTED_PLATFORMS[target_os]["icon"]
        # command.extend(["--icon", icon_path])
        pass # 图标处理已注释，直到资源文件存在

    # PyInstaller 会自动打包，但有时需要帮助才能找到所有内容。
    # 对于像 OpenCV 这样的库，这个钩子通常是必需的。
    command.extend(["--collect-all", "cv2"])

    print("\n-- 构建命令已生成。")
    if run_command(command):
        print(f"\n-- 构建成功！请在 'dist' 目录中找到您的应用程序。")
    else:
        print(f"\n-- 构建失败。请检查上面的输出以获取错误信息。")