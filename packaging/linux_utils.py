import os
import shutil

def create_linux_artifacts(dist_path: str, app_name: str):
    """
    为 Linux 创建特定的构建产物。

    - 将 'assets' 目录复制到 'dist' 文件夹。
    - 创建一个 .desktop 文件以便与应用程序菜单集成。

    Args:
        dist_path (str): PyInstaller 输出的完整路径。
        app_name (str): 应用程序的名称。
    """
    dist_dir = os.path.abspath(dist_path)
    executable_path = os.path.join(dist_dir, app_name)

    # 复制 assets 文件夹到 dist
    assets_src = "assets"
    assets_dest = os.path.join(dist_dir, "assets")
    icon_path = ""
    if not os.path.exists(assets_src):
        print(f"警告: '{assets_src}' 文件夹不存在，无法复制图标。")
    else:
        if os.path.exists(assets_dest):
            shutil.rmtree(assets_dest)
        shutil.copytree(assets_src, assets_dest)
        
        png_icon_path = os.path.join(assets_dest, "app.png")
        if os.path.exists(png_icon_path):
            icon_path = png_icon_path
        else:
            print(f"警告: 在 '{assets_dest}' 中未找到 'app.png' 用于 .desktop 文件。")

    # 为含有空格的路径给 Exec 字段加上引号
    desktop_file_content = f"""[Desktop Entry]
Version=1.0
Name={app_name}
Comment=Extract frames from video files
Exec="{executable_path}"
"""
    if icon_path:
        desktop_file_content += f"Icon={icon_path}\n"
    
    desktop_file_content += """Terminal=false
Type=Application
Categories=Utility;Video;
"""

    desktop_file_path = os.path.join(dist_dir, f"{app_name}.desktop")
    with open(desktop_file_path, "w") as f:
        f.write(desktop_file_content)

    print(f"创建了 .desktop 文件: {desktop_file_path}")
    if icon_path:
        print(f"请注意：.desktop 文件中的路径是绝对路径。如果您移动了 dist 文件夹，快捷方式将失效。")