"""
数据管理器 - 统一处理所有数据操作
"""
import json
import pickle
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict

from .config import CORPUS_DIR, CONCEPTS_DIR, MODELS_DIR


class DataManager:
    """数据管理器类"""
    
    def __init__(self):
        self.corpus_dir = CORPUS_DIR
        self.concepts_dir = CONCEPTS_DIR
        self.models_dir = MODELS_DIR
        
        # 确保目录存在
        self.corpus_dir.mkdir(exist_ok=True)
        self.concepts_dir.mkdir(exist_ok=True)
        self.models_dir.mkdir(exist_ok=True)
    
    def load_concept_data(self, concept_name: str) -> Dict[str, Any]:
        """加载概念数据"""
        concept_file = self.concepts_dir / f"{concept_name}.json"
        if concept_file.exists():
            with open(concept_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_concept_data(self, concept_name: str, data: Dict[str, Any]):
        """保存概念数据"""
        concept_file = self.concepts_dir / f"{concept_name}.json"
        with open(concept_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_corpus_data(self, era: str) -> List[str]:
        """加载特定时代的语料数据"""
        corpus_file = self.corpus_dir / f"{era}.txt"
        if corpus_file.exists():
            with open(corpus_file, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        return []
    
    def save_corpus_data(self, era: str, texts: List[str]):
        """保存特定时代的语料数据"""
        corpus_file = self.corpus_dir / f"{era}.txt"
        with open(corpus_file, 'w', encoding='utf-8') as f:
            for text in texts:
                f.write(text + '\n')
    
    def get_all_concepts(self) -> List[str]:
        """获取所有概念名称"""
        concept_files = list(self.concepts_dir.glob("*.json"))
        return [f.stem for f in concept_files]
    
    def get_concept_metadata(self, concept_name: str) -> Dict[str, Any]:
        """获取概念元数据"""
        data = self.load_concept_data(concept_name)
        return {
            "concept": concept_name,
            "eras": data.get("eras", []),
            "has_data": bool(data),
            "last_updated": data.get("last_updated", ""),
            "corpus_count": data.get("corpus_count", 0),
        }
    
    def update_concept_corpus(self, concept_name: str, era: str, texts: List[str]):
        """更新概念的语料数据"""
        data = self.load_concept_data(concept_name)
        
        if "corpus" not in data:
            data["corpus"] = {}
        
        data["corpus"][era] = texts
        data["corpus_count"] = sum(len(texts) for texts in data["corpus"].values())
        data["last_updated"] = self._get_current_time()
        
        self.save_concept_data(concept_name, data)
    
    def get_concept_corpus(self, concept_name: str, era: str) -> List[str]:
        """获取概念的语料数据"""
        data = self.load_concept_data(concept_name)
        return data.get("corpus", {}).get(era, [])
    
    def _get_current_time(self) -> str:
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def export_all_data(self) -> Dict[str, Any]:
        """导出所有数据（用于备份）"""
        export_data = {
            "concepts": {},
            "corpus": {},
            "metadata": {
                "export_time": self._get_current_time(),
                "total_concepts": 0,
                "total_corpus": 0,
            }
        }
        
        # 导出概念数据
        for concept in self.get_all_concepts():
            concept_data = self.load_concept_data(concept)
            export_data["concepts"][concept] = concept_data
            export_data["metadata"]["total_concepts"] += 1
        
        # 导出语料数据
        for era in ["古希腊", "中世纪", "近代", "现代"]:
            corpus_data = self.load_corpus_data(era)
            export_data["corpus"][era] = corpus_data
            export_data["metadata"]["total_corpus"] += len(corpus_data)
        
        return export_data
    
    def import_data(self, import_data: Dict[str, Any]):
        """导入数据（用于恢复）"""
        # 导入概念数据
        for concept_name, concept_data in import_data.get("concepts", {}).items():
            self.save_concept_data(concept_name, concept_data)
        
        # 导入语料数据
        for era, texts in import_data.get("corpus", {}).items():
            self.save_corpus_data(era, texts)


# 全局数据管理器实例
data_manager = DataManager()
