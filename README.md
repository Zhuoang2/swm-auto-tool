# 半自动沙威玛辅助工具

Python 开发的快捷键实现自动鼠标控制沙威玛辅助工具。**非全自动，没有图像识别**

**由于此脚本配置复杂，且根据游戏流程进度不同，需要自行编写合适的脚本操作并绑定快捷键，而且每台设备需要重新配置坐标点，故不提供打包好的 exe 文件，做不到开箱即用**

## 配置

入口文件为 `main.py` 推荐用管理员身份运行。

根目录 `config.py` 内有部分杂项配置，此文件被导入 `main.py` 内。

在 `sha` 目录下：

- `__init__.py`：实现鼠标控制的抽象层。
- `points.py`：配置坐标点。
- 上述两个文件都在 `main.py` 内引入，并在 `main.py` 内调用并传入坐标点。

## 开发

依赖库：

- `pyperclip` 用于快速复制当前鼠标坐标
- `win32api, win32con` 模拟鼠标操作
- `pynput` 监听键盘，绑定快捷键
