"""AI Code Quality Assistant - FastAPI Backend"""

import os
import sys
sys.path.append('.')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1 import analysis_router, health_router, llm_router, qwen_router

# 初始化FastAPI应用
app = FastAPI(
    title="AI Code Quality Assistant",
    description="智能代码质量分析与优化助手",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(health_router)
app.include_router(analysis_router)
app.include_router(llm_router)
app.include_router(qwen_router)

@app.get("/")
async def root():
    """根端点"""
    return {
        "message": "AI Code Quality Assistant API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)