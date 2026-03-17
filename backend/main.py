"""AI Code Quality Assistant - FastAPI Backend"""

import os
import sys
sys.path.append('.')

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware

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

# Private Network Access 响应头中间件
# 允许公网页面访问 loopback / 私有网络地址
class PrivateNetworkAccessMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 预检请求：直接返回 200 + 授权头
        if request.method == "OPTIONS" and \
           request.headers.get("Access-Control-Request-Private-Network") == "true":
            return Response(
                status_code=200,
                headers={
                    "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
                    "Access-Control-Allow-Private-Network": "true",
                    "Access-Control-Allow-Methods": "*",
                    "Access-Control-Allow-Headers": "*",
                }
            )
        response = await call_next(request)
        response.headers["Access-Control-Allow-Private-Network"] = "true"
        return response

app.add_middleware(PrivateNetworkAccessMiddleware)

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