# 视频帧提取器

一个基于Python和PySide6开发的视频帧提取工具，可以从视频文件中提取指定帧并保存为图片。

## 功能特性

- 🎥 支持多种视频格式（MP4、AVI、MOV、MKV、WMV、FLV等）
- 🖼️ 支持多种图片输出格式（JPEG、PNG、BMP、TIFF、WEBP）
- ⏯️ 视频播放和暂停功能
- 🎯 精确帧定位（按帧号或时间跳转）
- 📐 灵活的输出尺寸设置（原始尺寸、自定义尺寸、常用分辨率）
- 🖱️ 支持拖拽导入视频文件
- 📁 支持按目录选择视频文件
- 🎨 现代化的图形用户界面

## 系统要求

- Python 3.8+
- PySide6
- OpenCV
- Pillow

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行程序

```bash
python main.py
```

## 使用说明

### 1. 加载视频
- 点击"打开视频文件"按钮选择视频文件
- 或直接将视频文件拖拽到程序窗口中

### 2. 视频预览和控制
- 使用播放/暂停按钮控制视频播放
- 拖动进度条快速跳转到指定位置
- 使用"上一帧"/"下一帧"按钮精确定位
- 在帧号输入框中直接输入要跳转的帧号
- 在时间输入框中输入要跳转的时间（秒）

### 3. 导出设置
- 选择输出图片格式（JPEG、PNG、BMP、TIFF、WEBP）
- 选择输出尺寸：
  - 原始尺寸：保持视频原始分辨率
  - 自定义尺寸：手动设置宽度和高度
- 可选择是否保持宽高比

### 4. 导出帧
- 定位到要导出的帧
- 点击"导出当前帧"按钮
- 选择保存位置和文件名
- 确认导出

## 项目结构

```
video-frame-extractor/
├── main.py                 # 程序入口
├── requirements.txt        # 依赖包列表
├── README.md              # 项目说明
└── src/                   # 源代码目录
    ├── __init__.py
    ├── core/              # 核心功能模块
    │   ├── __init__.py
    │   └── video_processor.py    # 视频处理核心类
    ├── ui/                # 用户界面模块
    │   ├── __init__.py
    │   ├── main_window.py        # 主窗口
    │   ├── video_widget.py       # 视频显示控件
    │   └── export_dialog.py      # 导出对话框
    └── utils/             # 工具模块
        ├── __init__.py
        ├── file_utils.py         # 文件处理工具
        └── image_utils.py        # 图像处理工具
```

## 技术架构

### 核心模块
- **VideoProcessor**: 负责视频文件的加载、帧提取、格式转换等核心功能
- **MainWindow**: 主窗口界面，整合所有功能模块
- **VideoWidget**: 自定义视频显示控件，支持自适应缩放
- **ExportDialog**: 高级导出设置对话框

### 工具模块
- **FileUtils**: 文件路径处理、格式验证等工具函数
- **ImageUtils**: 图像格式转换、尺寸计算等工具函数

### 设计特点
- 高内聚低耦合的模块化设计
- 基于信号槽机制的事件驱动架构
- 支持拖拽操作的现代化界面
- 完整的中文注释和文档

## 开发说明

### 添加新的视频格式支持
在 `src/utils/file_utils.py` 中的 `SUPPORTED_VIDEO_FORMATS` 列表中添加新的文件扩展名。

### 添加新的图片格式支持
在 `src/utils/image_utils.py` 中的 `SUPPORTED_FORMATS` 字典中添加新的格式定义。

### 自定义界面样式
修改各UI模块中的样式表（setStyleSheet）来自定义界面外观。

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 更新日志

### v1.0.0
- 初始版本发布
- 基本的视频帧提取功能
- 支持多种视频和图片格式
- 现代化的图形用户界面