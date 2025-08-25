# Configuration Guide (配置指南)

## 📁 路径配置

### 1. 模型文件路径

在 `backend/config.py` 中修改以下配置：

```python
# 模型配置
MODEL_CONFIG = {
    "model_path": "YOUR_MODEL_PATH_HERE",  # 修改为你的模型文件路径
    # 例如: "C:/path/to/your/model.gguf"
}

# 本地模型配置
LOCAL_MODEL_CONFIG = {
    "model_path": "YOUR_MODEL_PATH_HERE",  # 修改为你的模型文件路径
    # 例如: "C:/path/to/your/model.gguf"
}
```

**支持的模型格式**:
- Qwen-7B-Chat: `qwen-7b-chat-f16.gguf`, `qwen-7b-chat-q4_0.gguf`
- LLaMA-2: `llama-2-7b-chat.gguf`, `llama-2-13b-chat.gguf`
- 其他GGUF格式模型

### 2. LLaMA.cpp 路径

在启动脚本中修改LLaMA.cpp路径：

**方法1: 修改启动脚本**
编辑 `start_llm_system.bat` 或 `start_services_only.bat`，找到以下行：
```batch
echo cd YOUR_LLAMA_CPP_PATH
echo .\llama-server.exe -m YOUR_MODEL_FILE -c 2048 --host 0.0.0.0 --port 8080
```

将其替换为实际路径：
```batch
cd C:\path\to\your\llama.cpp\build\bin\Release
.\llama-server.exe -m C:\path\to\your\model.gguf -c 2048 --host 0.0.0.0 --port 8080
```

**方法2: 使用环境变量**
创建 `.env` 文件：
```env
LLAMA_CPP_PATH=C:\path\to\your\llama.cpp\build\bin\Release
MODEL_PATH=C:\path\to\your\model.gguf
```

### 3. 项目路径

项目路径使用相对路径，无需修改：
```batch
# 后端服务
cd /d %~dp0 && python run_backend.py

# 前端服务  
cd /d %~dp0\frontend && npm start
```

## ⚙️ 其他配置

### GPU配置

如需启用GPU加速，在 `backend/config.py` 中修改：
```python
LOCAL_MODEL_CONFIG = {
    "gpu_enabled": True,    # 启用GPU
    "gpu_layers": 35,       # GPU层数（根据显存调整）
    "main_gpu": 0,          # 主GPU索引
}
```

### 端口配置

默认端口配置：
- **LLaMA.cpp服务器**: 8080
- **后端API服务**: 8000  
- **前端开发服务器**: 3000

如需修改，在相应配置文件中更新。

## 🔧 配置示例

### 完整配置示例

```python
# backend/config.py
LOCAL_MODEL_CONFIG = {
    "enabled": True,
    "host": "localhost",
    "port": 8080,
    "model_path": "D:/models/qwen-7b-chat-f16.gguf",  # 你的模型路径
    "api_type": "openai_compatible",
    "max_tokens": 2000,
    "temperature": 0.7,
    "context_length": 2048,
    "gpu_enabled": False,  # CPU模式
    "gpu_layers": 35,
    "main_gpu": 0,
}
```

### 启动脚本示例

```batch
# start_llm_system.bat
cd D:\llama.cpp\build\bin\Release
.\llama-server.exe -m D:\models\qwen-7b-chat-f16.gguf -c 2048 --host 0.0.0.0 --port 8080
```

## 📋 配置检查清单

启动前请确认：

- [ ] 模型文件路径正确
- [ ] LLaMA.cpp已编译
- [ ] 端口未被占用
- [ ] Python和Node.js已安装
- [ ] 依赖包已安装

## 🚨 常见配置错误

### 1. 路径错误
```
Error: Model file not found!
```
**解决方案**: 检查 `backend/config.py` 中的模型路径

### 2. LLaMA.cpp未编译
```
Error: LLaMA.cpp not compiled!
```
**解决方案**: 按照README编译LLaMA.cpp

### 3. 端口被占用
```
Port 8000 is already in use
```
**解决方案**: 脚本会自动处理，或手动关闭占用端口的程序

## 💡 配置技巧

1. **使用绝对路径**: 避免相对路径可能的问题
2. **路径分隔符**: Windows使用 `\` 或 `/`，Linux/Mac使用 `/`
3. **环境变量**: 使用环境变量管理敏感路径信息
4. **配置文件**: 将配置集中在一个文件中管理

## 🔍 配置验证

配置完成后，运行以下命令验证：

```bash
# 检查Python配置
python -c "from backend.config import LOCAL_MODEL_CONFIG; print(LOCAL_MODEL_CONFIG)"

# 检查模型文件
python -c "import os; print(os.path.exists('YOUR_MODEL_PATH'))"
```

---

**注意**: 首次使用前必须完成路径配置，否则系统无法正常运行。
