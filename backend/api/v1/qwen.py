"""Qwen API路由 - 支持通义千问集成"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import asyncio

from services.qwen_service import QwenService

router = APIRouter(prefix="/qwen", tags=["qwen"])

# 初始化Qwen服务
qwen_service = QwenService()

class QwenAnalysisRequest(BaseModel):
    code: str
    language: str
    model: Optional[str] = "qwen-plus"
    analysis_type: Optional[str] = "quality"  # quality, security, performance, refactoring

class RefactoringRequest(BaseModel):
    code: str
    language: str
    model: Optional[str] = "qwen-plus"

@router.post("/analyze")
async def analyze_code_with_qwen(request: QwenAnalysisRequest):
    """使用Qwen分析代码质量"""
    try:
        # 验证模型支持
        supported_models = ["qwen-turbo", "qwen-plus", "qwen-max", "qwen-max-longcontext"]
        if request.model not in supported_models:
            raise HTTPException(
                status_code=400, 
                detail=f"不支持的模型。支持的模型: {', '.join(supported_models)}"
            )
        
        # 调用Qwen分析
        result = await qwen_service.analyze_code_with_qwen(
            code=request.code,
            language=request.language,
            model=request.model
        )
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return JSONResponse(content={
            "success": True,
            "data": result
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Qwen分析失败: {str(e)}")

@router.post("/refactor")
async def generate_qwen_refactoring_suggestions(request: RefactoringRequest):
    """生成Qwen代码重构建议"""
    try:
        # 验证模型支持
        supported_models = ["qwen-turbo", "qwen-plus", "qwen-max", "qwen-max-longcontext"]
        if request.model not in supported_models:
            raise HTTPException(
                status_code=400, 
                detail=f"不支持的模型。支持的模型: {', '.join(supported_models)}"
            )
        
        # 生成重构建议
        result = await qwen_service.generate_refactoring_suggestions(
            code=request.code,
            language=request.language,
            model=request.model
        )
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return JSONResponse(content={
            "success": True,
            "data": result
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Qwen重构建议生成失败: {str(e)}")

@router.get("/models")
async def get_available_qwen_models():
    """获取可用的Qwen模型列表"""
    models = qwen_service.get_available_models()
    
    return JSONResponse(content={
        "success": True,
        "data": {
            "models": models,
            "total_count": len(models),
            "recommended": "qwen-plus",
            "provider": "Alibaba DashScope",
            "language_support": "Chinese/English bilingual",
            "features": [
                "高质量中文代码分析",
                "多语言代码支持",
                "结构化JSON输出",
                "详细的重构建议"
            ]
        }
    })

@router.get("/status")
async def get_qwen_service_status():
    """获取Qwen服务状态"""
    return JSONResponse(content={
        "success": True,
        "data": {
            "configured": bool(qwen_service.api_key),
            "available_models": list(qwen_service.model_config.keys()),
            "service_status": "ready",
            "provider": "Alibaba DashScope",
            "api_endpoint": qwen_service.base_url,
            "features": {
                "chinese_analysis": True,
                "code_quality_assessment": True,
                "security_analysis": True,
                "refactoring_suggestions": True,
                "multilingual_support": True
            }
        }
    })