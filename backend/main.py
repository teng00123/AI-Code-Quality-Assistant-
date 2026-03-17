"""AI Code Quality Assistant - FastAPI Backend"""

import os
import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from core.analyzer import StaticAnalyzer
from core.scoring import QualityScorer

# 数据模型
class AnalysisRequest(BaseModel):
    file_path: str
    language: Optional[str] = None

class AnalysisResult(BaseModel):
    analysis_id: str
    file_path: str
    language: str
    lines_of_code: int
    issues: List[dict]
    summary: dict
    quality_score: dict
    created_at: str

class HealthCheck(BaseModel):
    status: str
    version: str
    timestamp: str

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
    allow_headers=["*"]
)

# 初始化分析器和评分器
static_analyzer = StaticAnalyzer()
quality_scorer = QualityScorer()

# 内存存储（生产环境应使用数据库）
analysis_results = {}

@app.get("/", response_model=dict)
async def root():
    """根端点"""
    return {
        "message": "AI Code Quality Assistant API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """健康检查"""
    return HealthCheck(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now().isoformat()
    )

@app.post("/api/v1/analyze/file", response_model=AnalysisResult)
async def analyze_file(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """分析单个文件"""
    try:
        # 执行静态分析
        analysis_data = static_analyzer.analyze_file(request.file_path)
        
        if 'error' in analysis_data:
            raise HTTPException(status_code=400, detail=analysis_data['error'])
        
        # 计算质量分数
        quality_score = quality_scorer.calculate_score(analysis_data)
        
        # 生成结果ID
        analysis_id = str(uuid.uuid4())
        created_at = datetime.now().isoformat()
        
        # 组装结果
        result = AnalysisResult(
            analysis_id=analysis_id,
            file_path=analysis_data['file_path'],
            language=analysis_data['language'],
            lines_of_code=analysis_data['lines_of_code'],
            issues=analysis_data['issues'],
            summary=analysis_data['summary'],
            quality_score=quality_score,
            created_at=created_at
        )
        
        # 存储结果
        analysis_results[analysis_id] = result.dict()
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/analyze/upload")
async def analyze_uploaded_file(file: UploadFile = File(...)):
    """分析上传的文件"""
    try:
        # 保存临时文件
        temp_dir = "/tmp/code_analysis"
        os.makedirs(temp_dir, exist_ok=True)
        temp_file_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")
        
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 分析文件
        analysis_data = static_analyzer.analyze_file(temp_file_path)
        
        if 'error' in analysis_data:
            raise HTTPException(status_code=400, detail=analysis_data['error'])
        
        # 计算质量分数
        quality_score = quality_scorer.calculate_score(analysis_data)
        
        # 清理临时文件
        background_tasks.add_task(os.remove, temp_file_path)
        
        return {
            "success": True,
            "analysis": analysis_data,
            "quality_score": quality_score,
            "filename": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/analysis/{analysis_id}", response_model=AnalysisResult)
async def get_analysis_result(analysis_id: str):
    """获取分析结果"""
    if analysis_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return AnalysisResult(**analysis_results[analysis_id])

@app.get("/api/v1/analysis")
async def list_analysis_results(limit: int = 10):
    """列出分析结果"""
    results = list(analysis_results.values())[-limit:]
    return {
        "total": len(analysis_results),
        "results": results
    }

@app.delete("/api/v1/analysis/{analysis_id}")
async def delete_analysis_result(analysis_id: str):
    """删除分析结果"""
    if analysis_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    del analysis_results[analysis_id]
    return {"message": "Analysis deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)