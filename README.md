# Philosophy Concept Explorer (哲学概念解释器)

一个基于本地大语言模型的哲学概念解释和语义变迁追踪系统。

## 🌟 功能特性

- **哲学概念解释**: 通过本地LLM解释哲学概念的含义
- **语义变迁追踪**: 追踪概念在不同历史时期的含义变化
- **可视化图表**: 生成语义偏移度的可视化图表
- **本地部署**: 完全本地化，保护隐私和数据安全
- **中文支持**: 原生支持中文哲学概念

## 🏗️ 系统架构

```
Philosophy Concept Explorer
├── Frontend (React)          # 用户界面
├── Backend (FastAPI)         # API服务
├── LLaMA.cpp Server          # 本地大语言模型服务
└── Data Management           # 概念数据和语料管理
```

## 🚀 快速开始

### 环境要求

- **操作系统**: Windows 10/11
- **Python**: 3.8+
- **Node.js**: 16+
- **CUDA**: 12.0+ (可选，用于GPU加速)
- **内存**: 至少16GB RAM
- **存储**: 至少20GB可用空间

### 安装步骤

#### 1. 克隆项目
```bash
git clone https://github.com/yourusername/philosophy-concept-explorer.git
cd philosophy-concept-explorer
```

#### 2. 安装Python依赖
```bash
cd backend
pip install -r requirements.txt
```

#### 3. 安装前端依赖
```bash
cd frontend
npm install
```

#### 4. 下载模型文件
下载Qwen-7B-Chat模型到 `C:\Users\cyq12\llama.cpp\` 目录：
```bash
# 模型文件: qwen-7b-chat-f16.gguf
# 大小: 约14GB
```

#### 5. 编译LLaMA.cpp (可选)
如果需要GPU加速，可以编译支持CUDA的版本：
```bash
cd C:\Users\cyq12\llama.cpp
mkdir build && cd build
cmake .. -G "Visual Studio 17 2022" -A x64 -DGGML_CUDA=ON
cmake --build . --config Release
```

**注意**: 当前版本使用CPU模式运行，确保系统稳定性。GPU模式需要额外的CUDA配置。

### 启动系统

#### 方法1: 使用启动脚本 (推荐)
```bash
# 双击运行 - 完全自动化
start_llm_system.bat
```

#### 方法2: 手动启动
```bash
# 1. 启动LLaMA.cpp服务器 (CPU模式)
cd C:\Users\cyq12\llama.cpp\build\bin\Release
.\llama-server.exe -m ..\..\..\qwen-7b-chat-f16.gguf -c 2048 --host 0.0.0.0 --port 8080

# 2. 启动后端服务
cd backend
python run_backend.py

# 3. 启动前端服务
cd frontend
npm start
```

## 📁 项目结构

```
philosophy-concept-explorer/
├── backend/                  # 后端服务
│   ├── main.py              # FastAPI应用入口
│   ├── routes/              # API路由
│   ├── utils/               # 工具函数
│   ├── data/                # 数据文件
│   ├── config.py            # 配置文件
│   └── requirements.txt     # Python依赖
├── frontend/                # 前端应用
│   ├── src/                 # 源代码
│   ├── public/              # 静态资源
│   └── package.json         # Node.js依赖
├── start_llm_system.bat     # 一键启动脚本 (完全自动化)
├── start_services_only.bat  # 仅启动服务脚本 (完全自动化)
└── README.md                # 项目说明
```

## 🔧 配置说明

### 后端配置 (`backend/config.py`)
- **模型路径**: 本地LLM模型文件位置
- **API设置**: 服务端口和主机配置
- **数据目录**: 概念数据和语料库路径

### 前端配置 (`frontend/src/App.jsx`)
- **API端点**: 后端服务地址
- **UI主题**: 界面样式和布局
- **功能开关**: 各种功能的启用/禁用

## 📊 数据格式

### 概念数据 (`backend/data/concepts/`)
```json
{
  "word": "自由",
  "explanations": {
    "古希腊": "在古希腊哲学中，自由主要指...",
    "中世纪": "中世纪时期，自由概念与...",
    "现代": "现代哲学中，自由被理解为..."
  },
  "semantic_shift": {
    "古希腊": 0.8,
    "中世纪": 0.6,
    "现代": 0.9
  },
  "related_concepts": ["意志", "选择", "责任"],
  "philosophers": ["苏格拉底", "康德", "萨特"]
}
```

### 语料库 (`backend/data/corpus/`)
- 支持TXT格式的哲学文本
- 按时代和主题分类存储
- 用于语义分析和概念解释

## 🌐 API接口

### 概念相关
- `GET /api/concepts` - 获取概念列表
- `GET /api/concept_metadata/{word}` - 获取概念元数据
- `POST /api/explain_concept` - 解释哲学概念
- `GET /api/semantic_shift/{word}` - 获取语义变迁图表

### 系统状态
- `GET /api/llm_status` - 检查LLM服务状态

## 🎯 使用示例

### 1. 解释哲学概念
在前端界面输入概念名称（如"自由"、"理性"、"意识"），系统会：
- 调用本地LLM生成解释
- 显示不同时代的含义变化
- 生成语义变迁可视化图表

### 2. 查看语义变迁
系统会分析概念在不同历史时期的含义变化，并生成：
- 语义偏移度数值
- 时代对比分析
- 可视化趋势图表

## 🚀 自动化功能

### 智能启动脚本
- **自动端口检测**: 自动检测并释放被占用的端口
- **依赖检查**: 自动检查Python、Node.js、模型文件等依赖
- **服务状态监控**: 实时监控各服务的启动状态
- **彩色输出**: 使用颜色区分不同类型的信息
- **错误处理**: 智能处理各种启动错误和异常情况

### 服务管理
- **一键启动**: `start_llm_system.bat` - 完全自动化启动所有服务
- **快速启动**: `start_services_only.bat` - 仅启动服务（跳过依赖检查）

## 🔍 故障排除

### 常见问题

#### LLaMA.cpp服务启动失败
- 检查模型文件路径是否正确
- 确认端口8080未被占用
- 检查模型文件完整性

#### 前端无法连接后端
- 确认后端服务正在运行
- 检查端口8000是否可访问
- 查看浏览器控制台错误信息

#### AI分析超时
- 检查LLM服务状态
- 增加超时时间设置
- 确认模型加载完成

### 日志查看
- **后端日志**: 查看启动终端的输出
- **LLaMA.cpp日志**: 查看LLaMA.cpp服务窗口
- **前端日志**: 查看浏览器开发者工具

## 🤝 贡献指南

欢迎贡献代码和想法！

### 贡献方式
1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

### 开发环境
- 使用Python 3.8+和Node.js 16+
- 遵循PEP 8 Python代码规范
- 添加适当的注释和文档

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [LLaMA.cpp](https://github.com/ggerganov/llama.cpp) - 本地LLM推理框架
- [Qwen](https://github.com/QwenLM/Qwen) - 大语言模型
- [FastAPI](https://fastapi.tiangolo.com/) - 现代Python Web框架
- [React](https://reactjs.org/) - 用户界面库

## 📞 联系方式

- **项目主页**: [GitHub Repository](https://github.com/yourusername/philosophy-concept-explorer)
- **问题反馈**: [Issues](https://github.com/yourusername/philosophy-concept-explorer/issues)
- **讨论交流**: [Discussions](https://github.com/yourusername/philosophy-concept-explorer/discussions)

---

**Philosophy Concept Explorer** - 探索哲学概念的语义变迁，理解思想的演进历程。
