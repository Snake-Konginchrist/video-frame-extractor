"""
构建配置模块。

此文件包含构建过程的中央配置。
它会自动从 pyproject.toml 加载项目信息。
"""

import platform
import sys
import tomllib

def load_project_info():
    """从 pyproject.toml 加载项目包名、显示名、版本和作者。"""
    try:
        with open("pyproject.toml", "rb") as f:
            data = tomllib.load(f)
            project_data = data["project"]
            metadata = project_data["metadata"]

            # 统一使用 app_name 作为应用名称
            app_name = metadata.get("app_name", project_data["name"]) 
            version = project_data["version"]
            author = metadata["author"]

            if not all([app_name, version, author]):
                print("错误: pyproject.toml 中 app_name, version, author 不能为空。", file=sys.stderr)
                sys.exit(1)

            return app_name, version, author
            
    except FileNotFoundError:
        print("错误: pyproject.toml 未找到。", file=sys.stderr)
        sys.exit(1)
    except KeyError as e:
        print(f"错误: pyproject.toml 文件中缺少必需的键: {e}。", file=sys.stderr)
        sys.exit(1)

# --- 项目信息 (动态加载) ---
APP_NAME, APP_VERSION, AUTHOR_NAME = load_project_info()

# --- 应用信息 ---
COMPANY_NAME = AUTHOR_NAME

# --- 构建系统配置 ---
DEFAULT_ARCH = platform.machine().lower()

SUPPORTED_PLATFORMS = {
    "windows": {
        "icon": "assets/app.ico",
        "supported_archs": ["x86_64", "amd64", "win32"],
    },
    "macos": {
        "icon": "assets/app.icns",
        "supported_archs": ["x86_64", "arm64", "universal2"],
    },
    "linux": {
        "icon": "assets/app.png",
        "supported_archs": ["x86_64", "amd64"],
    }
}

# --- 构建模式 ---
BUILD_MODES = {
    "1": {
        "name": "单文件 (单个可执行文件)",
        "flag": "--onefile"
    },
    "2": {
        "name": "单目录 (包含依赖项的文件夹)",
        "flag": "--onedir"
    }
}