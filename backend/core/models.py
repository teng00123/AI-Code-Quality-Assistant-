"""共享数据模型和枚举"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Any

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