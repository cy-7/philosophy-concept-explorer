# Philosophy Concept Explorer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)

基于本地大语言模型的哲学概念解释和语义变迁追踪系统。通过AI分析哲学概念在不同历史时期的含义变化，生成可视化图表展示语义漂移。

![Philosophy Concept Explorer界面](app-screenshot.png)

## ✨ 功能特性

- 🧠 **本地大语言模型驱动** - 使用Qwen-7B-Chat模型进行概念分析
- 📚 **哲学概念解释** - 智能解释哲学概念的含义和背景
- 🕰️ **语义变迁追踪** - 分析概念从古希腊到现代的语义变化
- 📊 **AI生成图表** - 动态生成语义漂移可视化图表
- 🌍 **中文支持** - 完整的中文哲学概念支持
- 🚀 **一键启动** - 完全自动化的服务启动脚本

## 🏗️ 系统架构

```
Philosophy Concept Explorer
├── Backend (FastAPI)          # 后端API服务
├── Frontend (React)           # 前端用户界面
├── LLaMA.cpp Server          # 本地大语言模型服务
└── Automated Scripts         # 自动化启动脚本
```

## 📋 系统要求

### 基础要求
- **操作系统**: Windows 10/11, macOS, Linux
- **Python**: 3.8 或更高版本
- **Node.js**: 16 或更高版本
- **内存**: 至少 8GB RAM
- **存储**: 至少 5GB 可用空间

### 模型要求
- **LLaMA.cpp**: 已编译的可执行文件
- **模型文件**: Qwen-7B-Chat GGUF格式模型
- **推荐配置**: 支持CUDA的GPU（可选，CPU模式也可运行）

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/yourusername/philosophy-concept-explorer.git
cd philosophy-concept-explorer
```

### 2. 安装依赖
```bash
# 安装Python依赖
pip install -r requirements.txt

# 安装前端依赖
cd frontend
npm install
cd ..
```

### 3. 配置模型路径
在 `backend/config.py` 中修改模型配置：
```python
LOCAL_MODEL_CONFIG = {
    "host": "localhost",
    "port": 8080,
    "model_path": "YOUR_MODEL_PATH_HERE",  # 修改为你的模型文件路径
    "api_type": "openai",
    "max_tokens": 2048,
    "temperature": 0.7,
    "context_length": 4096
}
```

**详细配置说明**: 请参考 [CONFIGURATION.md](CONFIGURATION.md) 文件。

### 4. 启动系统
```bash
# 使用自动化脚本（推荐）
start_llm_system.bat

# 或手动启动各服务
# 启动LLaMA.cpp服务器
cd YOUR_LLAMA_CPP_PATH
.\llama-server.exe -m YOUR_MODEL_FILE -c 2048 --host 0.0.0.0 --port 8080

# 启动后端服务
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 启动前端服务
cd frontend
npm start
```

## 📁 项目结构

```
philosophy-concept-explorer/
├── backend/                    # 后端代码
│   ├── main.py               # FastAPI应用入口
│   ├── config.py             # 配置文件
│   ├── data_manager.py       # 数据管理
│   ├── routes/               # API路由
│   │   └── concepts.py       # 概念相关API
│   └── utils/                # 工具函数
│       ├── concepts.py       # 概念处理
│       ├── explain.py        # AI解释逻辑
│       └── plot.py           # 图表生成
├── frontend/                  # 前端代码
│   ├── src/
│   │   ├── App.jsx          # 主应用组件
│   │   └── App.css          # 样式文件
│   └── package.json         # 前端依赖
├── data/                     # 数据文件
│   └── concepts/            # 概念数据
├── start_llm_system.bat     # 自动化启动脚本
├── start_services_only.bat  # 快速启动脚本
├── run_backend.py           # 后端启动脚本
├── README.md                # 项目说明
├── CHANGELOG.md             # 版本更新日志
├── ABOUT.md                 # 项目介绍
├── LICENSE                  # 开源许可证
└── .gitignore              # Git忽略配置
```

## 🔧 配置说明

### 模型配置
在 `backend/config.py` 中配置你的模型：
```python
# 模型路径配置
MODEL_PATH = "path/to/your/model.gguf"

# GPU配置（可选）
GPU_ENABLED = True
GPU_LAYERS = 35
MAIN_GPU = 0
```

### 端口配置
- **LLaMA.cpp服务器**: 8080
- **后端API服务**: 8000
- **前端开发服务器**: 3000

### 数据配置
概念数据存储在 `data/concepts/` 目录下，每个概念一个JSON文件：
```json
{
    "word": "自由",
    "explanations": ["概念解释..."],
    "corpus": ["相关语料..."],
    "semantic_shift": {
        "ancient_greece": 0.8,
        "middle_ages": 0.6,
        "modern": 0.9
    }
}
```

## 📖 使用指南

### 1. 启动系统
双击 `start_llm_system.bat` 或运行：
```bash
start_llm_system.bat
```

### 2. 访问应用
- 前端界面: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

### 3. 使用功能
1. 选择哲学概念（如"自由"、"理性"、"意识"）
2. 查看AI生成的概念解释
3. 分析语义变迁数据
4. 生成可视化图表

## 🔌 API接口

### 概念相关
- `GET /concepts` - 获取所有概念列表
- `GET /concept_metadata/{word}` - 获取概念元数据
- `GET /explain/{word}` - AI解释概念
- `GET /semantic_shift/{word}` - 获取语义变迁数据

### AI分析
- `POST /ai_analyze/{word}` - AI分析概念语义变迁
- `GET /llm_status` - 检查LLM服务状态

### 图表生成
- `GET /generate_chart/{word}` - 生成语义变迁图表

## 🛠️ 故障排除

### 常见问题

#### 1. LLaMA.cpp服务启动失败
- 检查模型文件路径是否正确
- 确认LLaMA.cpp已正确编译
- 检查端口8080是否被占用

#### 2. 后端服务无法启动
- 确认Python环境正确
- 检查依赖是否安装完整
- 确认端口8000未被占用

#### 3. 前端页面空白
- 检查Node.js版本
- 重新安装前端依赖
- 确认后端服务正在运行

#### 4. AI分析超时
- CPU模式下分析较慢，请耐心等待
- 检查LLM服务状态
- 考虑使用GPU加速

### 性能优化
- **CPU模式**: 适合开发和测试，分析速度较慢
- **GPU模式**: 推荐生产使用，分析速度快
- **模型优化**: 使用量化模型减少内存占用

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📝 开发计划

### v1.1.0 (计划中)
- [ ] 支持更多哲学概念
- [ ] 支持本地模型训练
- [ ] 添加批量概念分析
- [ ] 优化AI分析性能

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [cursor](https://cursor.com/) 

## 📞 联系方式

- 项目主页: [GitHub Repository](https://github.com/yourusername/philosophy-concept-explorer)
- 问题反馈: [Issues](https://github.com/yourusername/philosophy-concept-explorer/issues)
- 讨论交流: [Discussions](https://github.com/yourusername/philosophy-concept-explorer/discussions)

---

⭐ 如果这个项目对你有帮助，请给它一个star！
