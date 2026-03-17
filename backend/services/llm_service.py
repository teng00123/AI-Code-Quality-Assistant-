"""LLM服务集成模块 - 支持GPT-4和Claude API"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional
import aiohttp
from datetime import datetime

class LLMService:
    """LLM服务集成类"""
    
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.openai_base_url = "https://api.openai.com/v1"
        self.anthropic_base_url = "https://api.anthropic.com/v1"
        self.model_config = {
            'gpt-4': {
                'name': 'gpt-4',
                'max_tokens': 4000,
                'temperature': 0.3,
                'provider': 'openai'
            },
            'gpt-3.5-turbo': {
                'name': 'gpt-3.5-turbo',
                'max_tokens': 4000,
                'temperature': 0.3,
                'provider': 'openai'
            },
            'claude-3-sonnet': {
                'name': 'claude-3-sonnet-20240229',
                'max_tokens': 4000,
                'temperature': 0.3,
                'provider': 'anthropic'
            },
            'claude-3-haiku': {
                'name': 'claude-3-haiku-20240307',
                'max_tokens': 4000,
                'temperature': 0.3,
                'provider': 'anthropic'
            }
        }
    
    async def analyze_code_with_llm(self, code: str, language: str, model: str = 'gpt-4') -> Dict[str, Any]:
        """使用LLM分析代码质量"""
        if model not in self.model_config:
            raise ValueError(f"Unsupported model: {model}")
        
        config = self.model_config[model]
        
        if config['provider'] == 'openai':
            return await self._call_openai(code, language, model)
        elif config['provider'] == 'anthropic':
            return await self._call_anthropic(code, language, model)
        else:
            raise ValueError(f"Unknown provider: {config['provider']}")
    
    async def _call_openai(self, code: str, language: str, model: str) -> Dict[str, Any]:
        """调用OpenAI GPT API"""
        if not self.openai_api_key:
            return self._mock_llm_response(code, language, 'gpt-4')
        
        prompt = self._build_analysis_prompt(code, language)
        
        headers = {
            'Authorization': f'Bearer {self.openai_api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': self.model_config[model]['name'],
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are an expert code reviewer. Analyze the provided code and provide detailed feedback on quality, issues, and suggestions.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'max_tokens': self.model_config[model]['max_tokens'],
            'temperature': self.model_config[model]['temperature']
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{self.openai_base_url}/chat/completions',
                    headers=headers,
                    json=data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return self._parse_openai_response(result)
                    else:
                        error_text = await response.text()
                        return {'error': f'OpenAI API error: {response.status} - {error_text}'}
        except Exception as e:
            return {'error': f'OpenAI API call failed: {str(e)}'}
    
    async def _call_anthropic(self, code: str, language: str, model: str) -> Dict[str, Any]:
        """调用Anthropic Claude API"""
        if not self.anthropic_api_key:
            return self._mock_llm_response(code, language, 'claude-3-sonnet')
        
        prompt = self._build_analysis_prompt(code, language)
        
        headers = {
            'x-api-key': self.anthropic_api_key,
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
        
        data = {
            'model': self.model_config[model]['name'],
            'max_tokens': self.model_config[model]['max_tokens'],
            'temperature': self.model_config[model]['temperature'],
            'messages': [
                {
                    'role': 'user',
                    'content': f"As an expert code reviewer, analyze the following {language} code and provide detailed feedback:\n\n```{language}\n{code}\n```\n\nPlease provide:\n1. Overall code quality assessment (1-10)\n2. Key issues identified\n3. Specific improvement suggestions\n4. Security concerns (if any)\n5. Performance recommendations"
                }
            ]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{self.anthropic_base_url}/messages',
                    headers=headers,
                    json=data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return self._parse_anthropic_response(result)
                    else:
                        error_text = await response.text()
                        return {'error': f'Anthropic API error: {response.status} - {error_text}'}
        except Exception as e:
            return {'error': f'Anthropic API call failed: {str(e)}'}
    
    def _build_analysis_prompt(self, code: str, language: str) -> str:
        """构建代码分析提示词"""
        return f"""
Analyze the following {language} code for quality, issues, and improvements:

```{language}
{code}
```

Provide analysis in JSON format with these fields:
- overall_score (1-10)
- summary (brief overview)
- issues (array of {language} objects with: type, line, severity, message, suggestion)
- strengths (array of positive aspects)
- recommendations (array of improvement suggestions)
- security_concerns (array of security issues)
- performance_tips (array of performance suggestions)
"""
    
    def _parse_openai_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """解析OpenAI API响应"""
        try:
            content = response['choices'][0]['message']['content']
            # 尝试解析JSON响应
            try:
                parsed_content = json.loads(content)
                return {
                    'success': True,
                    'provider': 'openai',
                    'model': response.get('model', 'gpt-4'),
                    'analysis': parsed_content,
                    'raw_response': content,
                    'timestamp': datetime.now().isoformat()
                }
            except json.JSONDecodeError:
                # 如果不是JSON，返回文本内容
                return {
                    'success': True,
                    'provider': 'openai',
                    'model': response.get('model', 'gpt-4'),
                    'analysis': {'summary': content},
                    'raw_response': content,
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            return {'error': f'Failed to parse OpenAI response: {str(e)}'}
    
    def _parse_anthropic_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """解析Anthropic API响应"""
        try:
            content = response['content'][0]['text']
            # 尝试解析JSON响应
            try:
                parsed_content = json.loads(content)
                return {
                    'success': True,
                    'provider': 'anthropic',
                    'model': response.get('model', 'claude-3-sonnet'),
                    'analysis': parsed_content,
                    'raw_response': content,
                    'timestamp': datetime.now().isoformat()
                }
            except json.JSONDecodeError:
                # 如果不是JSON，返回文本内容
                return {
                    'success': True,
                    'provider': 'anthropic',
                    'model': response.get('model', 'claude-3-sonnet'),
                    'analysis': {'summary': content},
                    'raw_response': content,
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            return {'error': f'Failed to parse Anthropic response: {str(e)}'}
    
    def _mock_llm_response(self, code: str, language: str, model: str) -> Dict[str, Any]:
        """模拟LLM响应（用于测试）"""
        return {
            'success': True,
            'provider': model.split('-')[0],
            'model': model,
            'analysis': {
                'overall_score': 8.5,
                'summary': f'Mock {model} analysis: Code quality looks good with minor improvements possible.',
                'issues': [
                    {
                        'type': 'style',
                        'line': 1,
                        'severity': 'low',
                        'message': 'Consider adding docstring',
                        'suggestion': 'Add descriptive docstring for better documentation'
                    }
                ],
                'strengths': ['Good variable naming', 'Clear logic structure'],
                'recommendations': ['Add unit tests', 'Consider error handling'],
                'security_concerns': [],
                'performance_tips': ['Consider caching for repeated operations']
            },
            'raw_response': 'Mock response for testing',
            'timestamp': datetime.now().isoformat(),
            'mock': True
        }
    
    async def generate_refactoring_suggestions(self, code: str, language: str, model: str = 'gpt-4') -> Dict[str, Any]:
        """生成重构建议"""
        prompt = f"""
Suggest specific refactoring improvements for the following {language} code:

```{language}
{code}
```

Provide suggestions for:
1. Code structure improvements
2. Performance optimizations
3. Better error handling
4. Modern language features usage
5. Testing strategy

Format as actionable recommendations with code examples where helpful.
"""
        
        if model.startswith('gpt'):
            return await self._call_openai_for_refactoring(prompt, model)
        else:
            return await self._call_anthropic_for_refactoring(prompt, model)
    
    async def _call_openai_for_refactoring(self, prompt: str, model: str) -> Dict[str, Any]:
        """调用OpenAI生成重构建议"""
        if not self.openai_api_key:
            return self._mock_refactoring_response(language, model)
        
        headers = {
            'Authorization': f'Bearer {self.openai_api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': self.model_config[model]['name'],
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are an expert software engineer specializing in code refactoring and optimization.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'max_tokens': 3000,
            'temperature': 0.4
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{self.openai_base_url}/chat/completions',
                    headers=headers,
                    json=data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return self._parse_refactoring_response(result, 'openai')
                    else:
                        return {'error': f'OpenAI API error: {response.status}'}
        except Exception as e:
            return {'error': f'OpenAI API call failed: {str(e)}'}
    
    def _mock_refactoring_response(self, language: str, model: str) -> Dict[str, Any]:
        """模拟重构建议响应"""
        return {
            'success': True,
            'provider': model.split('-')[0],
            'model': model,
            'refactoring_suggestions': {
                'structure': ['Extract methods for better modularity'],
                'performance': ['Use list comprehensions where appropriate'],
                'error_handling': ['Add try-catch blocks for risky operations'],
                'modern_features': ['Consider using f-strings (Python 3.6+)'],
                'testing': ['Add unit tests for edge cases']
            },
            'mock': True
        }