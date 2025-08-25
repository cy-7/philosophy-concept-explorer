"""
配置文件 - 集中管理所有配置项
"""
import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent

# 数据目录配置
DATA_DIR = BASE_DIR / "data"
CORPUS_DIR = DATA_DIR / "corpus"  # 语料库目录
CONCEPTS_DIR = DATA_DIR / "concepts"  # 概念数据目录
MODELS_DIR = BASE_DIR / "models"  # 模型存储目录

# 确保目录存在
DATA_DIR.mkdir(exist_ok=True)
CORPUS_DIR.mkdir(exist_ok=True)
CONCEPTS_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

# 模型配置
MODEL_CONFIG = {
    "default_model": "qwen-7b-chat",  # 默认模型名称
    "model_path": "YOUR_MODEL_PATH_HERE",  # 请修改为你的模型文件路径
    "max_tokens": 512,  # 最大生成token数
    "temperature": 0.7,  # 生成温度
    "context_length": 2048,  # 上下文长度
}

# 向量模型配置
VECTOR_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_DIMENSION = 384

# 语义漂移配置
SEMANTIC_SHIFT_CONFIG = {
    "eras": ["古希腊", "中世纪", "近代", "现代"],
    "min_similarity": 0.1,
    "max_similarity": 0.9,
}

# API配置
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "debug": True,
    "reload": True,
}

# 本地模型配置
LOCAL_MODEL_CONFIG = {
    "enabled": True,
    "host": "localhost",
    "port": 8080,
    "model_path": "YOUR_MODEL_PATH_HERE",  # 请修改为你的模型文件路径
    "api_type": "openai_compatible",  # 使用OpenAI兼容的API格式
    "max_tokens": 2000,
    "temperature": 0.7,
    "context_length": 2048,
    "gpu_enabled": False,  # 默认禁用GPU，需要时手动启用
    "gpu_layers": 35,     # GPU层数
    "main_gpu": 0,        # 主GPU索引
}

