import platform
import subprocess
import sys
import os
from typing import List

from packaging.build_config import (
    APP_NAME,
    DEFAULT_ARCH,
    SUPPORTED_PLATFORMS,
    BUILD_MODES,
)
from packaging.linux_utils import create_linux_artifacts

def get_current_os() -> str:
    """获取当前操作系统，并格式化为与 SUPPORTED_PLATFORMS 键匹配的格式。"""
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    return system

def get_user_choice(options: List[str], option_name: str, default: str) -> str:
    """
    提示用户从选项列表中进行选择。

    Args:
        options (List[str]): 可用选项的列表。
        option_name (str): 要提示的选项的名称（例如，“操作系统”、“架构”）。
        default (str): 默认选项。

    Returns:
        str: 用户选择的选项。
    """
    print(f"可用的 {option_name}:")
    for i, option in enumerate(options):
        if option == default:
            print(f"  {i + 1}. {option} (默认)")
        else:
            print(f"  {i + 1}. {option}")
    print("  按 'q' 退出。")

    while True:
        try:
            prompt = f"选择 {option_name} (1-{len(options)}) 或按 Enter 使用默认值 ({default}): "
            choice = input(prompt)

            if choice.lower() == 'q':
                print("用户取消构建。")
                sys.exit(0)

            if not choice:
                return default

            index = int(choice) - 1
            if 0 <= index < len(options):
                return options[index]
            else:
                print("无效的选择。请再试一次。")
        except ValueError:
            print("无效的输入。请输入一个数字。")

def main():
    """
    构建项目的主函数。
    """
    # 1. 选择操作系统
    available_os = list(SUPPORTED_PLATFORMS.keys())
    default_os = get_current_os()
    if default_os not in available_os:
        default_os = available_os[0]

    chosen_os = get_user_choice(available_os, "操作系统", default=default_os)
    print(f"您选择了: {chosen_os}")

    # 2. 根据操作系统选择架构
    available_archs = SUPPORTED_PLATFORMS[chosen_os]["supported_archs"]
    default_arch = DEFAULT_ARCH
    if default_arch not in available_archs:
        default_arch = available_archs[0]

    chosen_arch = get_user_choice(available_archs, "架构", default=default_arch)
    print(f"您选择了: {chosen_arch}")

    # 3. 选择构建模式
    mode_names = [mode['name'] for mode in BUILD_MODES.values()]
    default_mode_name = BUILD_MODES["2"]["name"]  # 默认使用单目录模式
    chosen_mode_name = get_user_choice(mode_names, "构建模式", default=default_mode_name)
    print(f"您选择了: {chosen_mode_name}")

    name_to_flag = {mode['name']: mode['flag'] for mode in BUILD_MODES.values()}
    chosen_flag = name_to_flag[chosen_mode_name]

    # 4. 构建 PyInstaller 命令
    # 为每个构建创建一个唯一的输出目录，目录名使用安全名（无空格）
    safe_dir_name = APP_NAME.replace(" ", "-").lower()
    output_dir_name = f"{safe_dir_name}-{chosen_os}-{chosen_arch}"
    dist_path = os.path.join("dist", output_dir_name)

    command = [
        "pyinstaller",
        "main.py",
        "--name",
        APP_NAME,  # 直接使用显示名
        f"--distpath={dist_path}",
        chosen_flag,
        "--windowed",
    ]

    if chosen_os == "macos":
        command.extend(["--target-arch", chosen_arch])

    icon_path = SUPPORTED_PLATFORMS[chosen_os].get("icon")
    if icon_path:
        command.extend(["--icon", icon_path])

    # 将 pyproject.toml 文件包含在打包应用中
    command.extend(["--add-data", f"pyproject.toml{os.pathsep}."])

    # 5. 执行构建命令
    print(f"正在运行命令: {' '.join(command)}")
    subprocess.run(command, check=True)

    # 6. 构建后操作
    if chosen_os == "linux":
        # 为 Linux 创建 .desktop 文件
        create_linux_artifacts(dist_path=dist_path, app_name=APP_NAME)

    print("构建成功完成!")


if __name__ == "__main__":
    main()
