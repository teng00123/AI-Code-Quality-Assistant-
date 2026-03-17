"""静态代码分析器 - 基于AST和正则表达式的代码质量检查"""

import ast
import re
import os
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum

class IssueType(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass
class CodeIssue:
    line: int
    column: int
    message: str
    issue_type: IssueType
    rule_id: str
    suggestion: str = ""

class StaticAnalyzer:
    """静态代码分析器"""
    
    def __init__(self):
        self.rules = {
            'long_function': {'max_lines': 50, 'severity': IssueType.WARNING},
            'deep_nesting': {'max_depth': 4, 'severity': IssueType.WARNING},
            'long_line': {'max_length': 120, 'severity': IssueType.INFO},
            'hardcoded_password': {'pattern': r'(password|pwd|pass)\s*=\s*["\'][^"\']+["\']', 'severity': IssueType.ERROR},
            'debug_print': {'pattern': r'print\s*\(', 'severity': IssueType.WARNING},
            'todo_comment': {'pattern': r'TODO|FIXME|XXX', 'severity': IssueType.INFO}
        }
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """分析单个文件"""
        if not os.path.exists(file_path):
            return {'error': f'File not found: {file_path}'}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {'error': f'Failed to read file: {str(e)}'}
        
        issues = []
        language = self._detect_language(file_path)
        
        if language == 'python':
            issues.extend(self._analyze_python_ast(content))
        
        issues.extend(self._analyze_with_regex(content, file_path))
        issues.extend(self._analyze_complexity(content, file_path))
        
        return {
            'file_path': file_path,
            'language': language,
            'lines_of_code': len(content.splitlines()),
            'issues': [self._issue_to_dict(issue) for issue in issues],
            'summary': self._generate_summary(issues)
        }
    
    def _detect_language(self, file_path: str) -> str:
        """检测编程语言"""
        ext = os.path.splitext(file_path)[1].lower()
        lang_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.go': 'go',
            '.rs': 'rust',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp'
        }
        return lang_map.get(ext, 'unknown')
    
    def _analyze_python_ast(self, content: str) -> List[CodeIssue]:
        """使用AST分析Python代码"""
        issues = []
        try:
            tree = ast.parse(content)
            visitor = PythonASTVisitor()
            visitor.visit(tree)
            issues.extend(visitor.issues)
        except SyntaxError as e:
            issues.append(CodeIssue(
                line=e.lineno,
                column=e.offset,
                message=f'Syntax error: {e.msg}',
                issue_type=IssueType.ERROR,
                rule_id='syntax_error',
                suggestion='Fix syntax error'
            ))
        return issues
    
    def _analyze_with_regex(self, content: str, file_path: str) -> List[CodeIssue]:
        """使用正则表达式分析代码"""
        issues = []
        lines = content.splitlines()
        
        for line_num, line in enumerate(lines, 1):
            for rule_id, rule_config in self.rules.items():
                if 'pattern' in rule_config:
                    if re.search(rule_config['pattern'], line, re.IGNORECASE):
                        issues.append(CodeIssue(
                            line=line_num,
                            column=1,
                            message=f'Found {rule_id.replace("_", " ")}',
                            issue_type=rule_config['severity'],
                            rule_id=rule_id,
                            suggestion=self._get_suggestion(rule_id)
                        ))
            
            # 检查行长
            if len(line) > self.rules['long_line']['max_length']:
                issues.append(CodeIssue(
                    line=line_num,
                    column=self.rules['long_line']['max_length'] + 1,
                    message=f'Line too long ({len(line)} > {self.rules["long_line"]["max_length"]})',
                    issue_type=self.rules['long_line']['severity'],
                    rule_id='long_line',
                    suggestion='Consider breaking line into multiple lines'
                ))
        
        return issues
    
    def _analyze_complexity(self, content: str, file_path: str) -> List[CodeIssue]:
        """分析代码复杂度"""
        issues = []
        lines = content.splitlines()
        
        # 简单的嵌套深度检查
        current_indent = 0
        max_indent = 0
        
        for line_num, line in enumerate(lines, 1):
            if line.strip():
                indent = len(line) - len(line.lstrip())
                if indent > max_indent:
                    max_indent = indent
        
        # 估算嵌套深度（每4个空格算一层）
        estimated_depth = max_indent // 4
        if estimated_depth > self.rules['deep_nesting']['max_depth']:
            issues.append(CodeIssue(
                line=1,
                column=1,
                message=f'Deep nesting detected (estimated depth: {estimated_depth})',
                issue_type=self.rules['deep_nesting']['severity'],
                rule_id='deep_nesting',
                suggestion='Reduce nesting by extracting functions or using guard clauses'
            ))
        
        return issues
    
    def _get_suggestion(self, rule_id: str) -> str:
        """获取修复建议"""
        suggestions = {
            'hardcoded_password': 'Use environment variables or secure credential storage',
            'debug_print': 'Remove debug prints or use proper logging',
            'todo_comment': 'Address TODO items or create tracking issue'
        }
        return suggestions.get(rule_id, 'Review and fix the issue')
    
    def _issue_to_dict(self, issue: CodeIssue) -> Dict[str, Any]:
        """转换Issue为字典"""
        return {
            'line': issue.line,
            'column': issue.column,
            'message': issue.message,
            'type': issue.issue_type.value,
            'rule_id': issue.rule_id,
            'suggestion': issue.suggestion
        }
    
    def _generate_summary(self, issues: List[CodeIssue]) -> Dict[str, int]:
        """生成问题摘要"""
        summary = {'error': 0, 'warning': 0, 'info': 0, 'total': len(issues)}
        for issue in issues:
            summary[issue.issue_type.value] += 1
        return summary

class PythonASTVisitor(ast.NodeVisitor):
    """Python AST访问器"""
    
    def __init__(self):
        self.issues = []
        self.function_lines = {}
    
    def visit_FunctionDef(self, node):
        # 检查函数长度
        start_line = node.lineno
        end_line = getattr(node, 'end_lineno', start_line)
        func_length = end_line - start_line + 1
        
        if func_length > 50:
            self.issues.append(CodeIssue(
                line=start_line,
                column=node.col_offset,
                message=f'Function too long ({func_length} lines)',
                issue_type=IssueType.WARNING,
                rule_id='long_function',
                suggestion='Consider splitting into smaller functions'
            ))
        
        self.generic_visit(node)