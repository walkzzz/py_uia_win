# rf-win - Windows Desktop Automation Robot Framework Library

[![Python Version](https://img.shields.io/pypi/pyversions/rf-win.svg)](https://pypi.org/project/rf-win/)
[![License](https://img.shields.io/pypi/l/rf-win.svg)](https://pypi.org/project/rf-win/)
[![PyPI Version](https://img.shields.io/pypi/v/rf-win.svg)](https://pypi.org/project/rf-win/)

## 项目简介

rf-win 是一个基于 pywinauto 和 UIAutomation 的 Robot Framework 库，用于 Windows 桌面应用自动化测试。它提供了统一的关键字接口，支持多种后端，简化了 Windows 桌面应用的自动化测试开发。

## 主要功能

- **应用管理**：启动、关闭、连接应用程序
- **窗口管理**：获取、切换、操作窗口
- **控件交互**：查找、点击、输入控件
- **鼠标/键盘操作**：模拟鼠标点击、移动、键盘输入
- **等待策略**：智能等待控件和窗口
- **数据 IO**：支持读写文本、JSON、CSV、Excel 文件
- **截图功能**：支持全屏和指定窗口截图
- **多后端支持**：支持 pywinauto 和 UIAutomation 后端
- **DPI 适配**：支持高 DPI 缩放
- **控件缓存**：提高控件查找效率

## 架构设计

rf-win 采用分层架构设计：

1. **业务层**：Robot Framework 关键字，直接暴露给测试用例
2. **服务层**：封装业务逻辑，处理应用、窗口、控件操作
3. **抽象层**：定义抽象接口，实现多后端支持
4. **后端层**：封装 pywinauto 和 UIAutomation 库的具体实现

## 安装

### 基本安装

```bash
pip install rf-win
```

### 安装 Excel 支持

```bash
pip install rf-win[excel]
```

### 开发模式安装

```bash
pip install -e .
pip install -e .[dev]
```

## 快速开始

### 示例 1：启动记事本并输入文本

```robotframework
*** Settings ***
Library    rf_win

*** Test Cases ***
测试启动记事本并输入文本
    # 启动记事本应用
    启动应用    C:/Windows/notepad.exe    别名=notepad
    
    # 等待窗口存在
    等待窗口存在    无标题 - 记事本    超时=10
    
    # 在编辑框中输入文本
    控件输入文本    Edit:    Hello Robot Framework!    窗口标题=无标题 - 记事本
    
    # 截图
    ${screenshot}    截图    文件名=notepad_test    窗口标题=无标题 - 记事本
    Log    截图已保存到: ${screenshot}
    
    # 关闭应用
    关闭应用    别名=notepad
```

### 示例 2：连接已运行的应用

```robotframework
*** Settings ***
Library    rf_win

*** Test Cases ***
测试连接已运行的应用
    # 连接已运行的应用
    连接应用    标题=无标题 - 记事本    别名=notepad
    
    # 在编辑框中输入文本
    控件输入文本    Edit:    Hello Again!    窗口标题=无标题 - 记事本
    
    # 关闭应用
    关闭应用    别名=notepad
```

## 关键字文档

### 应用管理关键字

- `启动应用`：启动指定路径的应用程序
- `连接应用`：连接到已运行的应用程序
- `关闭应用`：关闭指定别名的应用程序
- `关闭所有应用`：关闭所有已连接的应用程序
- `获取当前应用`：获取当前活动的应用程序
- `切换应用`：切换到指定别名的应用程序
- `应用是否运行`：检查应用程序是否正在运行

### 窗口管理关键字

- `获取当前窗口`：获取当前活动窗口
- `获取所有窗口`：获取所有窗口
- `切换窗口`：切换到指定标题或索引的窗口
- `激活窗口`：激活指定标题或索引的窗口
- `关闭窗口`：关闭指定标题或索引的窗口
- `窗口最大化`：将指定窗口最大化
- `窗口最小化`：将指定窗口最小化
- `窗口还原`：将指定窗口还原到正常大小
- `移动窗口`：移动指定窗口到指定位置
- `调整窗口大小`：调整指定窗口的大小
- `获取窗口标题`：获取指定窗口的标题
- `获取窗口位置`：获取指定窗口的位置
- `获取窗口大小`：获取指定窗口的大小
- `窗口是否存在`：检查指定窗口是否存在

### 控件管理关键字

- `查找控件`：根据定位器查找指定窗口中的控件
- `查找所有控件`：查找指定窗口中的所有匹配控件
- `点击控件`：点击指定控件
- `右键点击控件`：右键点击指定控件
- `双击控件`：双击指定控件
- `控件输入文本`：向指定控件输入文本
- `获取控件文本`：获取指定控件的文本内容
- `清空控件文本`：清空指定控件的文本内容
- `选择控件项`：选择下拉列表或列表框中的项
- `获取控件项`：获取下拉列表或列表框中的所有项
- `控件是否存在`：检查指定控件是否存在
- `控件是否可见`：检查指定控件是否可见
- `控件是否启用`：检查指定控件是否启用
- `获取控件属性`：获取指定控件的指定属性值
- `设置控件属性`：设置指定控件的指定属性值

### 操作关键字

- `点击鼠标`：在指定位置点击鼠标
- `右键点击鼠标`：在指定位置右键点击鼠标
- `双击鼠标`：在指定位置双击鼠标
- `移动鼠标`：将鼠标移动到指定位置
- `拖拽鼠标`：从起始位置拖拽鼠标到结束位置
- `滚动鼠标`：在指定位置滚动鼠标
- `按下鼠标`：在指定位置按下鼠标按钮
- `释放鼠标`：在指定位置释放鼠标按钮
- `获取鼠标位置`：获取当前鼠标的位置
- `输入文本`：输入指定的文本
- `按下按键`：按下指定的按键
- `释放按键`：释放指定的按键
- `组合按键`：按下并释放指定的组合按键
- `等待`：等待指定的时间
- `等待控件存在`：等待指定的控件存在
- `等待控件可见`：等待指定的控件可见
- `等待控件启用`：等待指定的控件启用
- `等待窗口存在`：等待指定的窗口存在
- `截图`：截取当前屏幕或指定窗口的截图

### 数据 IO 关键字

- `读取文本文件`：读取文本文件内容
- `写入文本文件`：向文本文件写入内容
- `读取 JSON 文件`：读取 JSON 文件内容
- `写入 JSON 文件`：向 JSON 文件写入内容
- `读取 CSV 文件`：读取 CSV 文件内容
- `写入 CSV 文件`：向 CSV 文件写入内容
- `读取 Excel 文件`：读取 Excel 文件内容
- `写入 Excel 文件`：向 Excel 文件写入内容

## 配置

### 全局配置

rf-win 提供了以下全局配置参数：

| 参数名 | 类型 | 默认值 | 描述 |
|-------|------|-------|------|
| timeout | float | 30.0 | 操作超时时间（秒） |
| retry_interval | float | 0.5 | 重试间隔时间（秒） |
| backend | str | "pywinauto" | 默认后端类型 |
| screenshot_folder | str | "screenshots" | 截图保存文件夹 |
| screenshot_format | str | "png" | 截图格式 |
| cache_enabled | bool | True | 是否启用控件缓存 |
| cache_timeout | float | 60.0 | 缓存超时时间（秒） |
| dpi_aware | bool | True | 是否启用 DPI 适配 |

### 配置方式

```python
# 修改全局配置
from rf_win.config.global_config import GlobalConfig

GlobalConfig.set('timeout', 60.0)
GlobalConfig.set('backend', 'uiautomation')
```

## 定位器语法

rf-win 使用以下定位器语法：

```
类型:属性1=值1;属性2=值2
```

### 支持的控件类型

- `Button`：按钮
- `Edit`：编辑框
- `ComboBox`：组合框
- `ListBox`：列表框
- `CheckBox`：复选框
- `RadioButton`：单选按钮
- `Menu`：菜单
- `MenuItem`：菜单项
- `Tab`：标签页
- `TabItem`：标签项
- `TreeView`：树状视图
- `TreeItem`：树状视图项
- `DataGrid`：数据网格
- `DataItem`：数据项
- `Static`：静态文本
- `ProgressBar`：进度条
- `Slider`：滑块
- `StatusBar`：状态栏

### 示例

```
# 按名称定位按钮
Button:name=确定

# 按类名定位编辑框
Edit:class_name=Edit

# 按自动化ID定位控件
Button:automation_id=btnOK

# 按多种属性定位控件
Edit:name=用户名;class_name=Edit
```

## 后端选择

rf-win 支持两种后端：

1. **pywinauto**：默认后端，支持大部分 Windows 应用
2. **uiautomation**：支持 UWP 应用和更多控件类型

### 切换后端

```robotframework
# 方式1：在启动应用时指定
启动应用    C:/Windows/notepad.exe    别名=notepad    后端=uiautomation

# 方式2：修改全局配置
${None}    Import Library    rf_win.config.global_config    as    GlobalConfig
${None}    Set Global Variable    ${GlobalConfig}    timeout    60.0
```

## 开发指南

### 目录结构

```
rf_win/
├── config/          # 配置文件
├── core/           # 核心抽象类
├── backend/        # 后端实现
├── services/       # 服务层
├── keywords/       # Robot Framework 关键字
├── utils/          # 工具函数
├── tests/          # 单元测试
├── docs/           # 文档
└── tools/          # 辅助工具
```

### 添加新关键字

1. 在 `keywords/` 目录下创建或修改关键字文件
2. 在 `services/` 目录下实现业务逻辑
3. 更新 `__init__.py` 文件，注册新关键字

### 运行测试

```bash
# 运行 Robot Framework 测试
robot test_notepad.robot

# 运行单元测试
pytest

# 运行单元测试并生成覆盖率报告
pytest --cov=rf_win tests/
```

## 常见问题

### Q1：控件查找失败

A1：请检查以下几点：
- 窗口标题是否正确
- 定位器语法是否正确
- 控件是否可见
- 后端类型是否匹配

### Q2：高 DPI 下坐标不准确

A2：确保启用了 DPI 适配：

```python
from rf_win.config.global_config import GlobalConfig
GlobalConfig.set('dpi_aware', True)
```

### Q3：应用启动失败

A3：请检查以下几点：
- 应用路径是否正确
- 应用是否需要管理员权限
- 应用是否已经在运行

## 许可证

rf-win 采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

- 作者：Your Name
- 邮箱：your.email@example.com
- 项目地址：https://github.com/yourusername/rf-win

## 更新日志

### v1.0.0 (2023-12-01)

- 初始版本发布
- 支持应用管理、窗口管理、控件交互、鼠标/键盘操作、数据 IO、截图功能
- 支持 pywinauto 和 UIAutomation 后端
- 支持高 DPI 缩放
- 支持控件缓存
