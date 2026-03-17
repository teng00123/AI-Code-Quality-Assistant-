"""代码质量评分系统"""

import math
from typing import Dict, List, Any
from ..analyzer.static_analyzer import IssueType

class QualityScorer:
    """代码质量评分器"""
    
    def __init__(self):
        # 权重配置
        self.weights = {
            'maintainability': 0.3,
            'readability': 0.25,
            'security': 0.25,
            'performance': 0.2
        }
        
        # 问题严重程度扣分
        self.severity_penalties = {
            'error': 25,
            'warning': 10,
            'info': 3
        }
        
        # 最大分数
        self.max_score = 100
    
    def calculate_score(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """计算代码质量分数"""
        issues = analysis_result.get('issues', [])
        lines_of_code = analysis_result.get('lines_of_code', 0)
        
        if lines_of_code == 0:
            return self._empty_score_result()
        
        # 按类型分组问题
        issues_by_type = {'error': [], 'warning': [], 'info': []}
        for issue in issues:
            issue_type = issue.get('type', 'info')
            if issue_type in issues_by_type:
                issues_by_type[issue_type].append(issue)
        
        # 计算各维度分数
        maintainability_score = self._calculate_maintainability_score(issues, lines_of_code)
        readability_score = self._calculate_readability_score(issues, lines_of_code)
        security_score = self._calculate_security_score(issues_by_type['error'])
        performance_score = self._calculate_performance_score(issues)
        
        # 加权总分
        total_score = (
            maintainability_score * self.weights['maintainability'] +
            readability_score * self.weights['readability'] +
            security_score * self.weights['security'] +
            performance_score * self.weights['performance']
        )
        
        return {
            'total_score': round(total_score, 2),
            'max_score': self.max_score,
            'grade': self._score_to_grade(total_score),
            'dimensions': {
                'maintainability': round(maintainability_score, 2),
                'readability': round(readability_score, 2),
                'security': round(security_score, 2),
                'performance': round(performance_score, 2)
            },
            'breakdown': {
                'issues_by_severity': {
                    'error': len(issues_by_type['error']),
                    'warning': len(issues_by_type['warning']),
                    'info': len(issues_by_type['info'])
                },
                'total_issues': len(issues),
                'lines_of_code': lines_of_code,
                'issues_per_kloc': round(len(issues) / (lines_of_code / 1000), 2) if lines_of_code > 0 else 0
            }
        }
    
    def _calculate_maintainability_score(self, issues: List[Dict], loc: int) -> float:
        """计算可维护性分数"""
        base_score = 85.0
        
        # 根据问题数量扣分
        error_penalty = len([i for i in issues if i.get('type') == 'error']) * 3
        warning_penalty = len([i for i in issues if i.get('type') == 'warning']) * 1
        info_penalty = len([i for i in issues if i.get('type') == 'info']) * 0.2
        
        # 根据代码行数调整（代码越多，容错率越高）
        size_factor = min(1.0, loc / 1000)  # 1000行代码为基准
        
        score = base_score - (error_penalty + warning_penalty + info_penalty) * size_factor
        return max(0, min(self.max_score, score))
    
    def _calculate_readability_score(self, issues: List[Dict], loc: int) -> float:
        """计算可读性分数"""
        base_score = 90.0
        
        # 检查特定可读性问题
        long_lines = len([i for i in issues if i.get('rule_id') == 'long_line'])
        deep_nesting = len([i for i in issues if i.get('rule_id') == 'deep_nesting'])
        long_functions = len([i for i in issues if i.get('rule_id') == 'long_function'])
        
        penalty = (long_lines * 2) + (deep_nesting * 5) + (long_functions * 3)
        
        # 注释密度奖励（简单估算）
        comment_ratio = self._estimate_comment_ratio(loc)
        comment_bonus = min(5, comment_ratio * 10)  # 最多5分奖励
        
        score = base_score - penalty + comment_bonus
        return max(0, min(self.max_score, score))
    
    def _calculate_security_score(self, errors: List[Dict]) -> float:
        """计算安全性分数"""
        base_score = 95.0
        
        # 安全问题通常是严重错误
        security_issues = [
            i for i in errors 
            if any(keyword in i.get('message', '').lower() 
                  for keyword in ['password', 'security', 'vulnerability', 'inject', 'auth'])
        ]
        
        penalty = len(security_issues) * 20
        score = base_score - penalty
        return max(0, min(self.max_score, score))
    
    def _calculate_performance_score(self, issues: List[Dict]) -> float:
        """计算性能分数"""
        base_score = 88.0
        
        # 性能相关问题
        perf_issues = [
            i for i in issues 
            if any(keyword in i.get('message', '').lower() 
                  for keyword in ['complexity', 'performance', 'optimization'])
        ]
        
        penalty = len(perf_issues) * 8
        score = base_score - penalty
        return max(0, min(self.max_score, score))
    
    def _estimate_comment_ratio(self, loc: int) -> float:
        """估算注释比例（简化版）"""
        # 这里应该分析实际文件，现在返回默认值
        return 0.15  # 假设15%的注释率
    
    def _score_to_grade(self, score: float) -> str:
        """分数转换为等级"""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
    
    def _empty_score_result(self) -> Dict[str, Any]:
        """空结果处理"""
        return {
            'total_score': 0,
            'max_score': self.max_score,
            'grade': 'N/A',
            'dimensions': {
                'maintainability': 0,
                'readability': 0,
                'security': 0,
                'performance': 0
            },
            'breakdown': {
                'issues_by_severity': {'error': 0, 'warning': 0, 'info': 0},
                'total_issues': 0,
                'lines_of_code': 0,
                'issues_per_kloc': 0
            }
        }