"""JavaScript代码分析器 - 基于AST和正则表达式的分析"""

import re
import os
from typing import Dict, List, Any
from ..models import CodeIssue, IssueType

class JavaScriptAnalyzer:
    """JavaScript静态代码分析器"""
    
    def __init__(self):
        self.rules = {
            'console_log': {
                'pattern': r'console\.(log|debug|info|warn|error)\s*\(',
                'severity': IssueType.WARNING,
                'message': 'Console statement found',
                'suggestion': 'Remove console statements or use proper logging library'
            },
            'alert_statement': {
                'pattern': r'alert\s*\(',
                'severity': IssueType.WARNING,
                'message': 'Alert statement found',
                'suggestion': 'Use proper UI notification instead of alert'
            },
            'eval_usage': {
                'pattern': r'eval\s*\(',
                'severity': IssueType.ERROR,
                'message': 'Eval usage detected',
                'suggestion': 'Avoid using eval() due to security risks'
            },
            'hardcoded_password': {
                'pattern': r'(password|pwd|pass)\s*[:=]\s*["\'][^"\']+["\']',
                'severity': IssueType.ERROR,
                'message': 'Hardcoded password detected',
                'suggestion': 'Use environment variables or secure credential storage'
            },
            'todo_comment': {
                'pattern': r'TODO|FIXME|XXX|HACK',
                'severity': IssueType.INFO,
                'message': 'TODO comment found',
                'suggestion': 'Address TODO items or create tracking issue'
            },
            'long_line': {
                'pattern': r'.{121,}',
                'severity': IssueType.INFO,
                'message': 'Line too long',
                'suggestion': 'Consider breaking line into multiple lines'
            }
        }
        
        # JavaScript特定规则
        self.js_specific_rules = {
            'var_usage': {
                'pattern': r'\bvar\s+',
                'severity': IssueType.WARNING,
                'message': 'Use of var detected',
                'suggestion': 'Use let or const instead of var'
            },
            'function_declaration': {
                'pattern': r'function\s+\w+\s*\([^)]*\)\s*\{[^}]*\}',
                'severity': IssueType.INFO,
                'message': 'Large function detected',
                'suggestion': 'Consider breaking large functions into smaller ones'
            },
            'callback_hell': {
                'pattern': r'\w+\s*\(\s*[^)]*\s*\(\s*[^)]*\s*\(',
                'severity': IssueType.WARNING,
                'message': 'Potential callback hell detected',
                'suggestion': 'Consider using Promises or async/await'
            }
        }
    
    def analyze(self, content: str, file_path: str) -> List[CodeIssue]:
        """分析JavaScript代码"""
        issues = []
        lines = content.splitlines()
        
        # 应用通用规则
        for line_num, line in enumerate(lines, 1):
            for rule_id, rule_config in self.rules.items():
                if re.search(rule_config['pattern'], line, re.IGNORECASE):
                    issues.append(CodeIssue(
                        line=line_num,
                        column=1,
                        message=rule_config['message'],
                        issue_type=rule_config['severity'],
                        rule_id=rule_id,
                        suggestion=rule_config['suggestion']
                    ))
            
            # 检查行长
            if len(line) > 120:
                issues.append(CodeIssue(
                    line=line_num,
                    column=121,
                    message=f'Line too long ({len(line)} > 120)',
                    issue_type=IssueType.INFO,
                    rule_id='long_line',
                    suggestion='Consider breaking line into multiple lines'
                ))
        
        # 应用JS特定规则
        for line_num, line in enumerate(lines, 1):
            for rule_id, rule_config in self.js_specific_rules.items():
                if re.search(rule_config['pattern'], line, re.IGNORECASE):
                    issues.append(CodeIssue(
                        line=line_num,
                        column=1,
                        message=rule_config['message'],
                        issue_type=rule_config['severity'],
                        rule_id=rule_id,
                        suggestion=rule_config['suggestion']
                    ))
        
        # 分析复杂度
        issues.extend(self._analyze_complexity(content, lines))
        
        return issues
    
    def _analyze_complexity(self, content: str, lines: List[str]) -> List[CodeIssue]:
        """分析JavaScript代码复杂度"""
        issues = []
        
        # 检查嵌套深度
        max_nesting = 0
        current_nesting = 0
        
        for line in lines:
            if line.strip():
                # 计算括号嵌套深度
                paren_depth = line.count('{') - line.count('}')
                current_nesting = max(current_nesting + paren_depth, 0)
                max_nesting = max(max_nesting, current_nesting)
        
        if max_nesting > 4:
            issues.append(CodeIssue(
                line=1,
                column=1,
                message=f'Deep nesting detected (depth: {max_nesting})',
                issue_type=IssueType.WARNING,
                rule_id='deep_nesting',
                suggestion='Reduce nesting by extracting functions or using guard clauses'
            ))
        
        return issues