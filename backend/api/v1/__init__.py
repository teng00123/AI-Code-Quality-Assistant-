# API v1 路由模块
from .analysis import router as analysis_router
from .health import router as health_router
from .llm import router as llm_router
from .qwen import router as qwen_router

__all__ = ['analysis_router', 'health_router', 'llm_router', 'qwen_router']
