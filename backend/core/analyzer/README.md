# 多语言代码分析器 - Phase 2 Alpha

## 🎯 概述

Phase 2 Alpha实现了**多语言支持**，目前支持：
- 🐍 **Python** - 基于AST的深度语法分析
- 🌐 **JavaScript** - 基于正则表达式和模式匹配的静态分析

## 🏗️ 架构设计

### 分析器层次结构
```
StaticAnalyzer (主控制器)
├── Python AST Analyzer (深度语法分析)
├── JavaScript Analyzer (静态模式匹配)
├── Regex-based Analyzer (通用规则)
└── Complexity Analyzer (复杂度分析)
```

### 支持的语言及特性

| 语言 | 扩展名 | 分析深度 | 特殊规则 | 检测能力 |
|------|--------|----------|----------|----------|
| Python | .py | AST深度分析 | 函数长度、复杂度 | 语法错误、风格问题、安全问题 |
| JavaScript | .js | 静态模式匹配 | ES6+特性、控制台语句 | 代码异味、安全问题、性能问题 |

## 🔧 JavaScript分析器特性

### 检测规则
- **console_log** - 检测console语句（警告）
- **alert_statement** - 检测alert使用（警告）
- **eval_usage** - 检测eval使用（错误）
- **hardcoded_password** - 检测硬编码密码（错误）
- **todo_comment** - 检测TODO/FIXME注释（信息）
- **long_line** - 检测超长行（信息）
- **var_usage** - 检测var使用（警告）
- **callback_hell** - 检测回调地狱（警告）

### 复杂度分析
- 嵌套深度检测
- 括号嵌套层级分析
- 函数长度估算

## 📊 测试结果

### JavaScript测试文件分析
- **文件**: test_javascript_sample.js (108行)
- **问题检测**: 25个问题
  - 错误: 3个（硬编码密码、eval使用）
  - 警告: 13个（console语句、var使用等）
  - 信息: 9个（TODO注释、长行等）
- **质量评分**: 74.95/100 (等级C)
- **处理时间**: <1秒

## 🚀 使用方法

```python
from backend.core.analyzer import StaticAnalyzer

analyzer = StaticAnalyzer()

# 分析Python文件
result_py = analyzer.analyze_file('script.py')

# 分析JavaScript文件  
result_js = analyzer.analyze_file('app.js')

# 结果格式统一
print(f"语言: {result['language']}")
print(f"问题数: {len(result['issues'])}")
print(f"质量分: {result['quality_score']['total_score']}")
```

## 🔄 后续计划

- [ ] 支持TypeScript (.ts)
- [ ] 支持Java (.java)  
- [ ] 支持Go (.go)
- [ ] LLM辅助深度分析
- [ ] 自定义规则引擎