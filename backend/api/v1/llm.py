"""LLM API路由 - 支持GPT-4和Claude集成"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import asyncio

from services.llm_service import LLMService

router = APIRouter(prefix="/llm", tags=["llm"])

# 初始化LLM服务
llm_service = LLMService()

class LLMAnalysisRequest(BaseModel):
    code: str
    language: str
    model: Optional[str] = "gpt-4"
    analysis_type: Optional[str] = "quality"  # quality, security, performance, refactoring

class RefactoringRequest(BaseModel):
    code: str
    language: str
    model: Optional[str] = "gpt-4"

@router.post("/analyze")
async def analyze_code_with_llm(request: LLMAnalysisRequest):
    """使用LLM分析代码质量"""
    try:
        # 验证模型支持
        supported_models = ["gpt-4", "gpt-3.5-turbo", "claude-3-sonnet", "claude-3-haiku"]
        if request.model not in supported_models:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported model. Supported: {', '.join(supported_models)}"
            )
        
        # 调用LLM分析
        result = await llm_service.analyze_code_with_llm(
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
        raise HTTPException(status_code=500, detail=f"LLM analysis failed: {str(e)}")

@router.post("/refactor")
async def generate_refactoring_suggestions(request: RefactoringRequest):
    """生成代码重构建议"""
    try:
        # 验证模型支持
        supported_models = ["gpt-4", "gpt-3.5-turbo", "claude-3-sonnet", "claude-3-haiku"]
        if request.model not in supported_models:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported model. Supported: {', '.join(supported_models)}"
            )
        
        # 生成重构建议
        result = await llm_service.generate_refactoring_suggestions(
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
        raise HTTPException(status_code=500, detail=f"Refactoring suggestion failed: {str(e)}")

@router.get("/models")
async def get_available_models():
    """获取可用的LLM模型列表"""
    models = {
        "openai": {
            "gpt-4": {
                "name": "GPT-4",
                "provider": "OpenAI",
                "description": "Most capable model for complex analysis",
                "max_tokens": 4000,
                "cost": "high"
            },
            "gpt-3.5-turbo": {
                "name": "GPT-3.5 Turbo",
                "provider": "OpenAI",
                "description": "Fast and cost-effective for most tasks",
                "max_tokens": 4000,
                "cost": "low"
            }
        },
        "anthropic": {
            "claude-3-sonnet": {
                "name": "Claude 3 Sonnet",
                "provider": "Anthropic",
                "description": "Balanced performance and speed",
                "max_tokens": 4000,
                "cost": "medium"
            },
            "claude-3-haiku": {
                "name": "Claude 3 Haiku",
                "provider": "Anthropic",
                "description": "Fastest model for quick analysis",
                "max_tokens": 4000,
                "cost": "low"
            }
        }
    }
    
    return JSONResponse(content={
        "success": True,
        "data": {
            "models": models,
            "total_count": 4,
            "recommended": "gpt-4"
        }
    })

@router.get("/status")
async def get_llm_service_status():
    """获取LLM服务状态"""
    return JSONResponse(content={
        "success": True,
        "data": {
            "openai_configured": bool(llm_service.openai_api_key),
            "anthropic_configured": bool(llm_service.anthropic_api_key),
            "available_models": list(llm_service.model_config.keys()),
            "service_status": "ready"
        }
    })