from typing import List, Dict, Any
import json
from pathlib import Path

from ..data_manager import data_manager

def get_explanations_for_concept(word: str) -> List[str]:
    """获取哲学概念在不同时代的解释。
    
    Args:
        word: 哲学概念词汇
        
    Returns:
        包含四个时代解释的列表
    """
    # 尝试从新的数据管理器获取数据
    concept_data = data_manager.load_concept_data(word)
    
    if concept_data and "explanations" in concept_data:
        # 使用新的JSON数据格式
        explanations = concept_data["explanations"]
        return [
            explanations.get("古希腊", ""),
            explanations.get("中世纪", ""),
            explanations.get("近代", ""),
            explanations.get("现代", "")
        ]
    
    # 如果没有找到数据，返回默认解释
    return [
        f"{word} 在古希腊语境中的核心含义与思想渊源...",
        f"{word} 在中世纪语境中的神学化与社会结构中的定位...",
        f"{word} 在近代语境中的启蒙思想与理性化进程...",
        f"{word} 在现代语境中的多学科解释与应用场景...",
    ]

def get_concept_list() -> List[str]:
    """获取所有可用的哲学概念列表。"""
    return data_manager.get_all_concepts()

def get_concept_metadata(word: str) -> Dict[str, Any]:
    """获取概念的元数据信息。"""
    return data_manager.get_concept_metadata(word)

def get_concept_corpus(word: str, era: str) -> List[str]:
    """获取概念在特定时代的语料数据。"""
    return data_manager.get_concept_corpus(word, era)

def get_semantic_shift_data(word: str) -> Dict[str, Any]:
    """获取概念的语义漂移数据。"""
    concept_data = data_manager.load_concept_data(word)
    if concept_data and "semantic_shift" in concept_data:
        return concept_data["semantic_shift"]
    
    # 如果没有预定义的语义漂移数据，返回默认值
    return {
        "values": [0.3, 0.4, 0.6, 0.7],
        "description": f"{word}概念的语义变化趋势"
    }

def get_related_concepts(word: str) -> List[str]:
    """获取相关概念列表。"""
    concept_data = data_manager.load_concept_data(word)
    return concept_data.get("related_concepts", [])

def get_philosophers(word: str, era: str) -> List[str]:
    """获取概念在特定时代的主要哲学家。"""
    concept_data = data_manager.load_concept_data(word)
    philosophers = concept_data.get("philosophers", {})
    return philosophers.get(era, [])



