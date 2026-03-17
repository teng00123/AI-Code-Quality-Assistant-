#!/usr/bin/env python3
"""测试代码示例 - 包含各种代码质量问题"""

import os
import sys
import json
from datetime import datetime

# TODO: 这是一个待办事项示例
# FIXME: 这是一个需要修复的问题示例

class ExampleClass:
    def __init__(self, name):
        self.name = name
        # 硬编码密码 - 安全问题
        self.password = "hardcoded123"
    
    def very_long_function(self, param1, param2, param3, param4, param5, param6, param7):
        """这是一个过长的函数示例"""
        # 打印调试信息
        print(f"Debug: Processing {param1}")
        
        # 多层嵌套示例
        if param1 > 0:
            if param2 > 0:
                if param3 > 0:
                    if param4 > 0:
                        if param5 > 0:
                            if param6 > 0:
                                if param7 > 0:
                                    result = param1 * param2 * param3 * param4 * param5 * param6 * param7
                                    print(f"Result: {result}")  # 另一个调试打印
                                    return result
        
        # 长行示例（超过120字符）
        very_long_variable_name = "This is a very long line that exceeds the recommended maximum line length of 120 characters and should trigger a warning in the code quality analyzer"
        
        return None
    
    def another_function_with_issues(self):
        # 更多的调试打印
        print("Starting function")
        print("Processing data")
        print("Ending function")
        
        # 硬编码值
        timeout = 3000  # 应该使用配置文件
        max_retries = 5
        
        return timeout, max_retries

def long_function_example():
    """另一个长函数示例"""
    # 这个函数故意写得很长，超过50行
    result = []
    for i in range(100):
        if i % 2 == 0:
            if i % 3 == 0:
                if i % 5 == 0:
                    result.append(f"Number {i} is divisible by 2, 3, and 5")
                else:
                    result.append(f"Number {i} is divisible by 2 and 3")
            else:
                result.append(f"Number {i} is divisible by 2")
        else:
            if i % 3 == 0:
                result.append(f"Number {i} is divisible by 3")
            else:
                result.append(f"Number {i} is not divisible by 2 or 3")
    
    # 更多代码行...
    processed_result = []
    for item in result:
        processed_item = item.upper()
        processed_result.append(processed_item)
    
    final_result = []
    for item in processed_result:
        if "DIVISIBLE" in item:
            final_result.append(item)
    
    return final_result

# XXX: 另一个标记示例
if __name__ == "__main__":
    example = ExampleClass("test")
    example.very_long_function(1, 2, 3, 4, 5, 6, 7)
    example.another_function_with_issues()
    long_function_example()
    
    # 密码硬编码示例
    db_password = "my_secret_password"
    api_key = "sk-1234567890abcdef"
    
    print("Test completed")