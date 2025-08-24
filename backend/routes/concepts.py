from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
from ..utils.concepts import get_explanations_for_concept, get_concept_list, get_concept_metadata
from ..utils.plot import generate_semantic_shift_image
from ..utils.explain import explain_concept, analyze_semantic_shift_with_ai, test_local_model

router = APIRouter()

@router.get("/concepts")
async def get_concepts():
    """获取所有可用的哲学概念列表"""
    try:
        concepts = get_concept_list()
        return {"concepts": concepts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取概念列表失败: {str(e)}")

@router.get("/concept_metadata/{word}")
async def get_concept_metadata_endpoint(word: str):
    """获取指定概念的元数据"""
    try:
        metadata = get_concept_metadata(word)
        return metadata
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取概念元数据失败: {str(e)}")

@router.get("/explain/{word}")
async def explain_concept_endpoint(word: str, use_ai: bool = True):
    """解释哲学概念，支持AI生成和预设数据"""
    try:
        result = explain_concept(word, use_ai=use_ai)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"概念解释失败: {str(e)}")

@router.get("/ai_analyze/{word}")
async def ai_analyze_concept(word: str):
    """使用AI分析概念的语义漂移"""
    try:
        # 检查LLM是否可用
        if not test_local_model():
            raise HTTPException(status_code=503, detail="本地LLM服务不可用，请确保LLaMA.cpp服务器已启动")
        
        result = analyze_semantic_shift_with_ai(word)
        if result.get("ai_generated"):
            return {
                "success": True,
                "data": result,
                "message": f"概念 '{word}' 的AI分析完成"
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "AI分析失败"),
                "raw_response": result.get("raw_response", ""),
                "message": f"概念 '{word}' 的AI分析失败"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI分析失败: {str(e)}")

@router.get("/semantic_shift/{word}")
async def get_semantic_shift_chart(word: str, use_ai: bool = True):
    """获取概念的语义漂移图表"""
    try:
        # 生成图表文件路径
        charts_dir = "backend/static/charts"
        os.makedirs(charts_dir, exist_ok=True)
        chart_file = f"{charts_dir}/{word}_semantic_shift.png"
        
        # 生成图表（支持AI生成数据）
        generate_semantic_shift_image(word, chart_file, use_ai=use_ai)
        
        # 返回图片文件
        if os.path.exists(chart_file):
            return FileResponse(chart_file, media_type="image/png")
        else:
            raise HTTPException(status_code=500, detail="图表生成失败")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取语义漂移图表失败: {str(e)}")

@router.get("/llm_status")
async def get_llm_status():
    """获取本地LLM服务状态"""
    try:
        is_available = test_local_model()
        return {
            "llm_available": is_available,
            "status": "online" if is_available else "offline",
            "message": "本地LLM服务正常" if is_available else "本地LLM服务不可用"
        }
    except Exception as e:
        return {
            "llm_available": False,
            "status": "error",
            "message": f"检查LLM状态失败: {str(e)}"
        }


