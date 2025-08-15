"""
配置工具类 - 从pyproject.toml读取应用配置信息
"""
import os
import sys
import tomllib
from pathlib import Path


class ConfigUtils:
    """配置工具类，用于读取pyproject.toml中的配置信息"""
    
    _config = None
    
    @classmethod
    def _load_config(cls):
        """加载配置文件"""
        if cls._config is None:
            # 获取项目根目录
            if getattr(sys, 'frozen', False):
                # 如果是打包后的exe
                project_root = Path(sys.executable).parent
            else:
                # 如果是源码运行
                project_root = Path(__file__).parent.parent.parent
            
            config_path = project_root / "pyproject.toml"
            
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
        
        return f"""{info['app_name']} {info['version']}
{info['description']}

{info['copyright']}
保留所有权利

功能特点：
{features_text}

技术支持：{info['email']}
项目主页：{info['website']}"""