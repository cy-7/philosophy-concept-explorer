"""
概念解释模块 - 支持RAG和本地大模型
"""
import requests
import json
import time
from typing import Dict, List, Optional, Tuple
from ..data_manager import data_manager
from ..config import LOCAL_MODEL_CONFIG

# 简单的内存缓存
_ai_analysis_cache = {}

def explain_concept_with_local_model(concept_name: str, era: str = "general") -> str:
    """使用本地LLM解释哲学概念"""
    try:
        # 构建提示词
        if era == "general":
            prompt = f"""请分析哲学概念"{concept_name}"的含义。请从以下角度进行分析：
1. 核心定义和本质特征
2. 在不同哲学流派中的理解
3. 与现代生活的关联

请用中文回答，格式要清晰易读。"""
        else:
            prompt = f"""请分析哲学概念"{concept_name}"在{era}时期的含义和特点。请从以下角度进行分析：
1. 该时期对该概念的主流理解
2. 代表性哲学家的观点
3. 与当时社会文化背景的关联
4. 对后世的影响

请用中文回答，格式要清晰易读。"""

        # 调用本地LLM
        response = requests.post(
            f"http://{LOCAL_MODEL_CONFIG['host']}:{LOCAL_MODEL_CONFIG['port']}/v1/chat/completions",
            json={
                "model": "qwen-7b-chat",
                "messages": [
                    {"role": "system", "content": "你是一位专业的哲学学者，擅长分析哲学概念的历史演变和现代意义。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"LLM调用失败: {response.status_code}"
            
    except Exception as e:
        return f"LLM调用出错: {str(e)}"

def analyze_semantic_shift_with_ai(concept_name: str, use_cache: bool = True) -> Dict:
    """使用AI分析概念的语义漂移"""
    try:
        # 检查缓存
        if use_cache and concept_name in _ai_analysis_cache:
            print(f"使用缓存的分析结果: {concept_name}")
            return _ai_analysis_cache[concept_name]
        
        # 检查是否已有保存的AI分析结果
        if use_cache:
            concept_data = data_manager.load_concept_data(concept_name)
            if concept_data and "semantic_shift" in concept_data and concept_data["semantic_shift"].get("ai_generated"):
                print(f"使用已保存的AI分析结果: {concept_name}")
                _ai_analysis_cache[concept_name] = concept_data["semantic_shift"]
                return concept_data["semantic_shift"]
        
        # 检查GPU状态
        if LOCAL_MODEL_CONFIG.get("gpu_enabled", False):
            print(f"开始AI分析概念: {concept_name} (GPU模式，RTX 4060加速，预计1-2分钟)")
        else:
            print(f"开始AI分析概念: {concept_name} (CPU模式，请耐心等待...)")
        
        # 构建语义漂移分析提示词
        prompt = f"""请分析哲学概念"{concept_name}"在不同历史时期的语义变化。请提供：

1. 古希腊时期（Ancient Greece）：该概念的含义、特点、代表性观点
2. 中世纪时期（Medieval）：该概念的发展变化、新的理解
3. 近代时期（Modern）：该概念的现代转向、新的内涵
4. 当代时期（Contemporary）：该概念的现状、最新发展

请为每个时期给出0.0-1.0之间的语义复杂度评分，其中：
- 0.0-0.3：概念简单、具体、直观
- 0.3-0.6：概念中等复杂、有一定抽象性
- 0.6-1.0：概念高度复杂、高度抽象、内涵丰富

请用JSON格式回答，格式如下：
{{
    "eras": {{
        "Ancient Greece": {{"score": 0.3, "description": "描述", "key_philosophers": ["哲学家1", "哲学家2"]}},
        "Medieval": {{"score": 0.4, "description": "描述", "key_philosophers": ["哲学家1", "哲学家2"]}},
        "Modern": {{"score": 0.6, "description": "描述", "key_philosophers": ["哲学家1", "哲学家2"]}},
        "Contemporary": {{"score": 0.7, "description": "描述", "key_philosophers": ["哲学家1", "哲学家2"]}}
    }},
    "overall_trend": "整体趋势描述",
    "key_insights": ["关键洞察1", "关键洞察2", "关键洞察3"]
}}"""

        # 调用本地LLM
        response = requests.post(
            f"http://{LOCAL_MODEL_CONFIG['host']}:{LOCAL_MODEL_CONFIG['port']}/v1/chat/completions",
            json={
                "model": "qwen-7b-chat",
                "messages": [
                    {"role": "system", "content": "你是一位专业的哲学史学者，擅长分析哲学概念的语义演变。请严格按照要求的JSON格式回答。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,  # 降低温度，提高一致性
                "max_tokens": 1000,  # 减少token数，提高速度
                "top_p": 0.9,  # 添加top_p参数
                "frequency_penalty": 0.1  # 添加频率惩罚
            },
            timeout=600  # CPU模式，增加到10分钟
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # 尝试解析JSON
            try:
                # 提取JSON部分
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                if start_idx != -1 and end_idx != -1:
                    json_str = content[start_idx:end_idx]
                    ai_analysis = json.loads(json_str)
                    
                    # 转换为标准格式
                    result_data = {
                        "values": [
                            ai_analysis["eras"]["Ancient Greece"]["score"],
                            ai_analysis["eras"]["Medieval"]["score"],
                            ai_analysis["eras"]["Modern"]["score"],
                            ai_analysis["eras"]["Contemporary"]["score"]
                        ],
                        "descriptions": {
                            "Ancient Greece": ai_analysis["eras"]["Ancient Greece"]["description"],
                            "Medieval": ai_analysis["eras"]["Medieval"]["description"],
                            "Modern": ai_analysis["eras"]["Modern"]["description"],
                            "Contemporary": ai_analysis["eras"]["Contemporary"]["description"]
                        },
                        "philosophers": {
                            "Ancient Greece": ai_analysis["eras"]["Ancient Greece"]["key_philosophers"],
                            "Medieval": ai_analysis["eras"]["Medieval"]["key_philosophers"],
                            "Modern": ai_analysis["eras"]["Modern"]["key_philosophers"],
                            "Contemporary": ai_analysis["eras"]["Contemporary"]["key_philosophers"]
                        },
                        "overall_trend": ai_analysis["overall_trend"],
                        "key_insights": ai_analysis["key_insights"],
                        "ai_generated": True
                    }
                    
                    # 保存到缓存
                    _ai_analysis_cache[concept_name] = result_data
                    print(f"AI分析完成: {concept_name}")
                    return result_data
                else:
                    raise ValueError("No JSON found in response")
                    
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                # 如果解析失败，返回错误信息
                error_result = {
                    "error": f"AI分析结果解析失败: {str(e)}",
                    "raw_response": content,
                    "ai_generated": False
                }
                return error_result
        else:
            return {
                "error": f"LLM调用失败: {response.status_code}",
                "ai_generated": False
            }
            
    except Exception as e:
        return {
            "error": f"AI分析出错: {str(e)}",
            "ai_generated": False
        }

def explain_concept(concept_name: str, use_ai: bool = True) -> Dict:
    """解释哲学概念，优先使用AI，回退到预设数据"""
    try:
        if use_ai:
            # 尝试使用AI分析
            ai_result = analyze_semantic_shift_with_ai(concept_name)
            
            if ai_result.get("ai_generated") and "error" not in ai_result:
                # AI分析成功，保存结果
                save_ai_analysis(concept_name, ai_result)
                return {
                    "explanations": {
                        "Ancient Greece": ai_result["descriptions"]["Ancient Greece"],
                        "Medieval": ai_result["descriptions"]["Medieval"],
                        "Modern": ai_result["descriptions"]["Modern"],
                        "Contemporary": ai_result["descriptions"]["Contemporary"]
                    },
                    "semantic_shift": ai_result,
                    "ai_generated": True
                }
            else:
                print(f"AI分析失败: {ai_result.get('error', 'Unknown error')}")
                # 回退到预设数据
                pass
        
        # 使用预设数据
        explanations = get_explanations_for_concept(concept_name)
        return {
            "explanations": explanations,
            "ai_generated": False
        }
        
    except Exception as e:
        print(f"概念解释出错: {str(e)}")
        # 回退到预设数据
        explanations = get_explanations_for_concept(concept_name)
        return {
            "explanations": explanations,
            "ai_generated": False
        }

def save_ai_analysis(concept_name: str, ai_result: Dict):
    """保存AI分析结果到数据管理器"""
    try:
        # 更新概念的语义漂移数据
        concept_data = data_manager.load_concept_data(concept_name)
        if concept_data:
            concept_data["semantic_shift"] = ai_result
            data_manager.save_concept_data(concept_name, concept_data)
            print(f"AI分析结果已保存到概念: {concept_name}")
    except Exception as e:
        print(f"保存AI分析结果失败: {str(e)}")

def get_explanations_for_concept(concept_name: str) -> Dict[str, str]:
    """获取概念的预设解释（回退方案）"""
    try:
        concept_data = data_manager.load_concept_data(concept_name)
        if concept_data and "explanations" in concept_data:
            return concept_data["explanations"]
        else:
            return {
                "Ancient Greece": f"{concept_name}在古希腊时期的基本含义和特点。",
                "Medieval": f"{concept_name}在中世纪时期的发展变化。",
                "Modern": f"{concept_name}在近代的现代转向。",
                "Contemporary": f"{concept_name}在当代的最新发展。"
            }
    except Exception as e:
        print(f"获取预设解释失败: {str(e)}")
        return {
            "Ancient Greece": f"{concept_name}在古希腊时期的基本含义和特点。",
            "Medieval": f"{concept_name}在中世纪时期的发展变化。",
            "Modern": f"{concept_name}在近代的现代转向。",
            "Contemporary": f"{concept_name}在当代的最新发展。"
        }

def test_local_model() -> bool:
    """测试本地LLM是否可用"""
    try:
        # 使用正确的LLaMA.cpp API端点
        response = requests.get(
            f"http://{LOCAL_MODEL_CONFIG['host']}:{LOCAL_MODEL_CONFIG['port']}/v1/models",
            timeout=5
        )
        return response.status_code == 200
    except:
        try:
            # 备用测试方法：尝试简单的completion请求
            response = requests.post(
                f"http://{LOCAL_MODEL_CONFIG['host']}:{LOCAL_MODEL_CONFIG['port']}/v1/chat/completions",
                json={
                    "model": "qwen-7b-chat",
                    "messages": [{"role": "user", "content": "test"}],
                    "max_tokens": 10
                },
                timeout=5
            )
            return response.status_code == 200
        except:
            return False


if __name__ == "__main__":
    # 测试本地模型
    if test_local_model():
        print("测试概念解释...")
        result = explain_concept("自由")
        for i, exp in enumerate(result):
            print(f"{i+1}. {exp}")
    else:
        print("本地模型不可用，使用预设数据")
        result = get_explanations_for_concept("自由")
        for i, exp in enumerate(result):
            print(f"{i+1}. {exp}")



