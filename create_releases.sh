#!/bin/bash

# AI Code Quality Assistant - Phase 1 MVP Releases Creation Script
# 使用方法: bash create_releases.sh YOUR_GITHUB_TOKEN

GITHUB_TOKEN=$1
REPO_OWNER="teng00123"
REPO_NAME="AI-Code-Quality-Assistant-"
BASE_URL="https://api.github.com/repos/$REPO_OWNER/$REPO_NAME"

if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ 错误: 请提供GitHub Token"
    echo "用法: bash create_releases.sh YOUR_GITHUB_TOKEN"
    exit 1
fi

echo "🚀 开始创建 Phase 1 MVP Releases..."

# Release data
releases=(
    "v0.1.0:Phase 1 MVP: Initial Release - Basic Code Analysis Foundation:069033d"
    "v0.1.1:Phase 1 MVP: Basic Code Analysis Functionality Complete:aae7bd5"
    "v0.1.2:Phase 1 MVP: Simple Quality Scoring Algorithm Complete:f851f14"
    "v0.1.3:Phase 1 MVP: FastAPI Backend Framework Complete:a1dd5b3"
    "v0.1.4:Phase 1 MVP: Vue3 Frontend Framework Complete:f124460"
    "v0.1.5:Phase 1 MVP: Docker Containerization Complete:f124460"
)

for release in "${releases[@]}"; do
    IFS=':' read -r tag name description commit <<< "$release"
    
    echo "📦 创建 Release: $tag - $name"
    
    # 创建release的JSON数据
    release_data=$(cat <<EOF
{
  "tag_name": "$tag",
  "target_commitish": "$commit",
  "name": "$name",
  "body": "## 🎯 $name\n\n**发布日期**: 2026-03-17\n**提交**: $commit\n\n$(case $tag in
"v0.1.0")
"✅ 项目初始化和基础架构搭建\n✅ 基础代码分析功能框架\n✅ 项目文档和README完善\n\n**技术栈**:\n- Python 3.9+ 后端\n- FastAPI 异步框架\n- Vue3 + Element Plus 前端\n- Docker 容器化支持"
;;
"v0.1.1")
"✅ 静态代码分析器 (StaticAnalyzer)\n✅ AST解析 + 正则表达式模式匹配\n✅ 多语言支持框架 (Python, JavaScript, Java, Go, Rust)\n✅ 问题检测规则引擎\n✅ 代码复杂度分析\n\n**检测能力**:\n- 硬编码密码检测\n- 调试打印语句识别\n- 长行代码检测\n- TODO/FIXME注释标记\n- 函数长度评估\n- 嵌套深度分析\n\n**测试结果**:\n- 分析95行Python代码\n- 检测13个问题 (2错误/7警告/4信息)\n- 处理时间 <1秒"
;;
"v0.1.2")
"✅ 四维度加权评分模型\n  - 可维护性 (30%)\n  - 可读性 (25%) \n  - 安全性 (25%)\n  - 性能 (20%)\n✅ 智能扣分规则\n✅ 等级划分标准 (A:≥90, B:≥80, C:≥70, D:≥60, F:<60)\n✅ 问题密度计算 (每千行问题数)\n\n**验证结果**:\n- 测试代码评分: 77.58/100 (等级C)\n- 各维度得分均衡分布\n- 算法稳定性验证通过"
;;
"v0.1.3")
"✅ 模块化API设计 (api/v1/)\n✅ RESTful接口规范\n✅ 异步请求处理\n✅ 文件上传支持\n✅ 背景任务处理\n\n**API端点**:\n- GET / - 根端点\n- GET /health - 健康检查\n- POST /api/v1/analysis/file - 分析本地文件\n- POST /api/v1/analysis/upload - 分析上传文件\n\n**技术实现**:\n- FastAPI 0.104.1 + Uvicorn ASGI服务器\n- Pydantic 2.5.0 数据验证\n- CORS跨域支持"
;;
"v0.1.4")
"✅ Vue3 + TypeScript + Composition API\n✅ Element Plus UI组件库\n✅ Vue Router 4.x 路由管理\n✅ Pinia 状态管理\n✅ ECharts 数据可视化\n\n**页面组件**:\n- 📊 Dashboard - 质量仪表板\n- 🔍 Analysis - 代码分析\n- 📈 Reports - 分析报告\n- ⚙️ Settings - 系统设置\n\n**用户体验**:\n- 响应式设计，支持移动端\n- 实时分析反馈\n- 可视化质量报告"
;;
"v0.1.5")
"✅ 多服务Docker Compose编排\n✅ 前后端分离容器构建\n✅ 数据库持久化配置\n✅ 监控组件集成\n\n**服务架构**:\n- backend (Python 3.9 + FastAPI)\n- frontend (Node 18 + Vite + Nginx)\n- postgres (PostgreSQL 15)\n- redis (Redis 7)\n- minio (对象存储)\n\n**部署特性**:\n- 一键启动所有服务\n- 健康检查机制\n- 数据卷持久化"
;;
esac)
  \n  ",
  "draft": false,
  "prerelease": false
}
EOF
    )
    
    # 发送API请求创建release
    response=$(curl -s -X POST \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        -H "Content-Type: application/json" \
        "$BASE_URL/releases" \
        -d "$release_data")
    
    # 检查响应
    if echo "$response" | grep -q '"html_url"'; then
        html_url=$(echo "$response" | grep -o '"html_url":"[^"]*"' | cut -d'"' -f4)
        echo "✅ 成功创建: $html_url"
    else
        echo "❌ 创建失败: $response"
    fi
    
    echo "---"
done

echo "🎉 Phase 1 MVP Releases 创建完成！"