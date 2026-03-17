"""健康检查和状态API路由"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "service": "AI Code Quality Assistant"
    }

@router.get("/detailed")
async def detailed_health_check():
    """详细健康检查"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "api_server": "operational",
            "analyzer": "operational", 
            "scoring_engine": "operational"
        },
        "metrics": {
            "analyses_performed": len([]),  # 实际实现中会统计
            "uptime": "00:00:00"  # 实际实现中会计算
        }
    }