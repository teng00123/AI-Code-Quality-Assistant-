"""分析相关API路由"""

from fastapi import APIRouter, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List, Optional
import os
import uuid
from datetime import datetime

from core.analyzer import StaticAnalyzer
from core.scoring import QualityScorer

router = APIRouter(prefix="/analysis", tags=["analysis"])

# 初始化分析器和评分器
static_analyzer = StaticAnalyzer()
quality_scorer = QualityScorer()

# 内存存储
analysis_results = {}

@router.post("/file", response_model=dict)
async def analyze_file(
    file_path: str, 
    language: Optional[str] = None,
    background_tasks: BackgroundTasks = None
):
    """分析本地文件"""
    try:
        analysis_data = static_analyzer.analyze_file(file_path)
        
        if 'error' in analysis_data:
            raise HTTPException(status_code=400, detail=analysis_data['error'])
        
        quality_score = quality_scorer.calculate_score(analysis_data)
        
        analysis_id = str(uuid.uuid4())
        created_at = datetime.now().isoformat()
        
        result = {
            "analysis_id": analysis_id,
            "file_path": analysis_data['file_path'],
            "language": analysis_data['language'],
            "lines_of_code": analysis_data['lines_of_code'],
            "issues": analysis_data['issues'],
            "summary": analysis_data['summary'],
            "quality_score": quality_score,
            "created_at": created_at
        }
        
        analysis_results[analysis_id] = result
        
        return {"success": True, "data": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
async def analyze_uploaded_file(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """分析上传的文件"""
    try:
        temp_dir = "/tmp/code_analysis"
        os.makedirs(temp_dir, exist_ok=True)
        temp_file_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")
        
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        analysis_data = static_analyzer.analyze_file(temp_file_path)
        
        if 'error' in analysis_data:
            raise HTTPException(status_code=400, detail=analysis_data['error'])
        
        quality_score = quality_scorer.calculate_score(analysis_data)
        
        if background_tasks:
            background_tasks.add_task(os.remove, temp_file_path)
        
        return {
            "success": True,
            "analysis": analysis_data,
            "quality_score": quality_score,
            "filename": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{analysis_id}")
async def get_analysis_result(analysis_id: str):
    """获取分析结果"""
    if analysis_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return {"success": True, "data": analysis_results[analysis_id]}

@router.get("/")
async def list_analysis_results(limit: int = 10):
    """列出分析结果"""
    results = list(analysis_results.values())[-limit:]
    return {
        "success": True,
        "total": len(analysis_results),
        "results": results
    }

@router.delete("/{analysis_id}")
async def delete_analysis_result(analysis_id: str):
    """删除分析结果"""
    if analysis_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    del analysis_results[analysis_id]
    return {"success": True, "message": "Analysis deleted successfully"}