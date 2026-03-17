"""Qwen LLM服务集成模块 - 支持通义千问API"""

import os
import json
import asyncio
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime

class QwenService:
    """Qwen LLM服务集成类"""
    
    def __init__(self):
        self.api_key = os.getenv('QWEN_API_KEY')
        self.base_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        self.model_config = {
            'qwen-turbo': {
                'name': 'qwen-turbo',
                'max_tokens': 4000,
                'temperature': 0.3,
                'description': '快速响应，适合简单分析任务'
            },
            'qwen-plus': {
                'name': 'qwen-plus',
                'max_tokens': 8000,
                'temperature': 0.3,
                'description': '平衡性能和质量，适合大多数场景'
            },
            'qwen-max': {
                'name': 'qwen-max',
                'max_tokens': 8000,
                'temperature': 0.3,
                'description': '最强性能，适合复杂分析任务'
            },
            'qwen-max-longcontext': {
                'name': 'qwen-max-longcontext',
                'max_tokens': 16000,
                'temperature': 0.3,
                'description': '超长上下文，适合大型代码分析'
            }
        }
    
    async def analyze_code_with_qwen(self, code: str, language: str, model: str = 'qwen-plus') -> Dict[str, Any]:
        """使用Qwen分析代码质量"""
        if model not in self.model_config:
            raise ValueError(f"Unsupported Qwen model: {model}")
        
        if not self.api_key:
            return self._mock_qwen_response(code, language, model)
        
        config = self.model_config[model]
        prompt = self._build_analysis_prompt(code, language)
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': config['name'],
            'input': {
                'messages': [
                    {
                        'role': 'system',
                        'content': '你是一个专业的代码审查专家。请分析提供的代码，评估代码质量，识别问题并提供改进建议。请用中文回答。'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            },
            'parameters': {
                'max_tokens': config['max_tokens'],
                'temperature': config['temperature'],
                'top_p': 0.8,
                'result_format': 'message'
            }
        }
        
        try:
            # 使用同步请求（Qwen API主要是同步的）
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: requests.post(self.base_url, headers=headers, json=data, timeout=30)
            )
            
            if response.status_code == 200:
                result = response.json()
                return self._parse_qwen_response(result, model)
            else:
                error_msg = f'Qwen API error: {response.status_code} - {response.text}'
                return {'error': error_msg}
                
        except Exception as e:
            return {'error': f'Qwen API call failed: {str(e)}'}
    
    def _build_analysis_prompt(self, code: str, language: str) -> str:
        """构建代码分析提示词（中文）"""
        return f"""
请分析以下{language}代码的质量，并提供详细反馈：

```{language}
{code}
```

请从以下几个方面进行分析：
1. 整体代码质量评分（1-10分）
2. 主要问题和缺陷
3. 安全漏洞（如有）
4. 性能优化建议
5. 代码结构和可读性评价
6. 具体的改进建议

请以JSON格式返回分析结果，包含以下字段：
- overall_score (整体评分1-10)
- summary (总体评价摘要)
- issues (问题数组，每项包含type, line, severity, message, suggestion)
- strengths (代码优点数组)
- recommendations (改进建议数组)
- security_concerns (安全问题数组)
- performance_tips (性能优化建议数组)
"""
    
    def _parse_qwen_response(self, response: Dict[str, Any], model: str) -> Dict[str, Any]:
        """解析Qwen API响应"""
        try:
            output = response.get('output', {})
            choices = output.get('choices', [])
            if not choices:
                return {'error': 'No response from Qwen'}
            
            content = choices[0].get('message', {}).get('content', '')
            
            # 尝试解析JSON响应
            try:
                # 提取JSON部分（如果响应包含其他文本）
                json_start = content.find('{')
                json_end = content.rfind('}') + 1
                if json_start != -1 and json_end != 0:
                    json_content = content[json_start:json_end]
                    parsed_content = json.loads(json_content)
                else:
                    parsed_content = json.loads(content)
                
                return {
                    'success': True,
                    'provider': 'qwen',
                    'model': model,
                    'analysis': parsed_content,
                    'raw_response': content,
                    'timestamp': datetime.now().isoformat()
                }
            except json.JSONDecodeError:
                # 如果不是JSON，返回文本内容
                return {
                    'success': True,
                    'provider': 'qwen',
                    'model': model,
                    'analysis': {'summary': content},
                    'raw_response': content,
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            return {'error': f'Failed to parse Qwen response: {str(e)}'}
    
    def _mock_qwen_response(self, code: str, language: str, model: str) -> Dict[str, Any]:
        """模拟Qwen响应（用于测试）"""
        return {
            'success': True,
            'provider': 'qwen',
            'model': model,
            'analysis': {
                'overall_score': 8.2,
                'summary': f'模拟Qwen-{model}分析：代码结构清晰，逻辑合理，有少量改进空间。',
                'issues': [
                    {
                        'type': '代码风格',
                        'line': 1,
                        'severity': '低',
                        'message': '建议添加函数和模块文档字符串',
                        'suggestion': '为函数和模块添加详细的中文文档字符串'
                    },
                    {
                        'type': '错误处理',
                        'line': 15,
                        'severity': '中',
                        'message': '缺少异常处理机制',
                        'suggestion': '添加try-catch块处理可能的异常情况'
                    }
                ],
                'strengths': [
                    '变量命名规范，易于理解',
                    '代码结构层次清晰',
                    '逻辑流程合理'
                ],
                'recommendations': [
                    '添加单元测试覆盖边界情况',
                    '考虑使用类型注解提高代码可读性',
                    '优化算法复杂度'
                ],
                'security_concerns': [],
                'performance_tips': [
                    '对于大数据量处理，考虑使用生成器',
                    '避免不必要的重复计算'
                ]
            },
            'raw_response': '模拟Qwen响应内容',
            'timestamp': datetime.now().isoformat(),
            'mock': True
        }
    
    async def generate_refactoring_suggestions(self, code: str, language: str, model: str = 'qwen-plus') -> Dict[str, Any]:
        """生成代码重构建议"""
        if not self.api_key:
            return self._mock_refactoring_response(language, model)
        
        config = self.model_config[model]
        prompt = self._build_refactoring_prompt(code, language)
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': config['name'],
            'input': {
                'messages': [
                    {
                        'role': 'system',
                        'content': '你是一个资深的软件工程师，专精于代码重构和优化。请用中文提供具体的重构建议。'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            },
            'parameters': {
                'max_tokens': config['max_tokens'],
                'temperature': 0.4,
                'top_p': 0.8,
                'result_format': 'message'
            }
        }
        
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: requests.post(self.base_url, headers=headers, json=data, timeout=30)
            )
            
            if response.status_code == 200:
                result = response.json()
                return self._parse_refactoring_response(result, model)
            else:
                return {'error': f'Qwen API error: {response.status_code}'}
                
        except Exception as e:
            return {'error': f'Qwen API call failed: {str(e)}'}
    
    def _build_refactoring_prompt(self, code: str, language: str) -> str:
        """构建重构建议提示词"""
        return f"""
请为以下{language}代码提供具体的重构建议：

```{language}
{code}
```

请从以下方面提供建议：
1. 代码结构优化
2. 性能改进
3. 错误处理增强
4. 现代语言特性使用
5. 测试策略建议
6. 可维护性提升

请提供具体的代码示例来说明建议。请用中文回答，格式化为清晰的要点列表。
"""
    
    def _parse_refactoring_response(self, response: Dict[str, Any], model: str) -> Dict[str, Any]:
        """解析重构建议响应"""
        try:
            output = response.get('output', {})
            choices = output.get('choices', [])
            if not choices:
                return {'error': 'No response from Qwen'}
            
            content = choices[0].get('message', {}).get('content', '')
            
            return {
                'success': True,
                'provider': 'qwen',
                'model': model,
                'refactoring_suggestions': {
                    'content': content,
                    'summary': 'Qwen重构建议已生成'
                },
                'raw_response': content,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'error': f'Failed to parse refactoring response: {str(e)}'}
    
    def _mock_refactoring_response(self, language: str, model: str) -> Dict[str, Any]:
        """模拟重构建议响应"""
        mock_content = f"""
针对{language}代码的重构建议：

## 1. 代码结构优化
- 提取重复逻辑为独立函数
- 使用策略模式处理不同情况
- 将大类拆分为单一职责的小类

## 2. 性能改进
- 使用缓存减少重复计算
- 采用惰性求值处理大数据集
- 优化算法时间复杂度

## 3. 错误处理增强
- 添加输入参数验证
- 使用具体的异常类型
- 提供有意义的错误消息

## 4. 现代语言特性
- 使用f-string格式化字符串
- 采用类型注解提高可读性
- 利用上下文管理器自动清理资源

## 5. 测试策略
- 为核心逻辑编写单元测试
- 添加集成测试验证组件协作
- 使用mock对象隔离外部依赖
"""
        
        return {
            'success': True,
            'provider': 'qwen',
            'model': model,
            'refactoring_suggestions': {
                'content': mock_content,
                'summary': '模拟Qwen重构建议'
            },
            'raw_response': mock_content,
            'timestamp': datetime.now().isoformat(),
            'mock': True
        }
    
    def get_available_models(self) -> Dict[str, Any]:
        """获取可用模型信息"""
        return {
            'qwen-turbo': {
                'name': 'Qwen-Turbo',
                'provider': 'Alibaba',
                'description': '快速响应，适合简单分析任务',
                'max_tokens': 4000,
                'chinese_support': True
            },
            'qwen-plus': {
                'name': 'Qwen-Plus',
                'provider': 'Alibaba',
                'description': '平衡性能和质量，适合大多数场景',
                'max_tokens': 8000,
                'chinese_support': True
            },
            'qwen-max': {
                'name': 'Qwen-Max',
                'provider': 'Alibaba',
                'description': '最强性能，适合复杂分析任务',
                'max_tokens': 8000,
                'chinese_support': True
            },
            'qwen-max-longcontext': {
                'name': 'Qwen-Max-LongContext',
                'provider': 'Alibaba',
                'description': '超长上下文，适合大型代码分析',
                'max_tokens': 16000,
                'chinese_support': True
            }
        }