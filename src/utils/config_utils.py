"""
配置工具类 - 从pyproject.toml读取应用配置信息
"""
import os
import sys
import tomllib
import platform
from pathlib import Path


class ConfigUtils:
    """配置工具类，用于读取pyproject.toml中的配置信息"""
    
    _config = None
    
    @classmethod
    def _load_config(cls):
        """加载配置文件，兼容源码、onefile、onedir模式"""
        if cls._config is None:
            if getattr(sys, 'frozen', False):
                # 已打包的应用
                if hasattr(sys, '_MEIPASS'):
                    # onefile 模式: _MEIPASS 是解压后的临时目录
                    base_path = Path(sys._MEIPASS)
                else:
                    # onedir 模式: 相对于可执行文件的路径
                    if platform.system() == "Darwin":
                        # macOS: .app/Contents/MacOS/executable -> .app/
                        base_path = Path(sys.executable).parent.parent.parent
                    else:
                        # Windows/Linux: executable is in the root folder
                        base_path = Path(sys.executable).parent
            else:
                # 源码运行模式
                base_path = Path(__file__).parent.parent.parent
            
            config_path = base_path / "pyproject.toml"
            
            with open(config_path, "rb") as f:
                cls._config = tomllib.load(f)

    
    @classmethod
    def get_app_info(cls):
        """获取应用信息"""
        cls._load_config()
        
        metadata = cls._config["project"]["metadata"]
        project = cls._config["project"]
        
        return {
            "app_name": metadata["app_name"],
            "version": metadata["version"],
            "copyright": metadata["copyright"],
            "author": metadata["author"],
            "email": metadata["email"],
            "description": metadata["description"],
            "website": metadata["website"]
        }
    
    @classmethod
    def get_app_name(cls):
        """获取应用名称"""
        return cls.get_app_info()["app_name"]
    
    @classmethod
    def get_version(cls):
        """获取版本号"""
        return cls.get_app_info()["version"]
    
    @classmethod
    def get_copyright(cls):
        """获取版权信息"""
        return cls.get_app_info()["copyright"]
    
    @classmethod
    def get_about_text(cls):
        """获取关于对话框的文本内容"""
        info = cls.get_app_info()
        cls._load_config()
        
        features = cls._config["project"]["metadata"]["about"]["features"]
        features_text = "\n".join(f"• {feature}" for feature in features)
        
        return f"{info['app_name']} {info['version']}\n{info['description']}\n\n{info['copyright']}\n保留所有权利\n\n功能特点：\n{features_text}\n\n技术支持：{info['email']}\n项目主页：{info['website']}"    
