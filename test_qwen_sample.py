# 测试Qwen分析的Python代码示例

def calculate_fibonacci(n):
    """计算斐波那契数列"""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib_sequence = [0, 1]
    for i in range(2, n):
        next_term = fib_sequence[i-1] + fib_sequence[i-2]
        fib_sequence.append(next_term)
    
    return fib_sequence

# TODO: 添加输入验证
# FIXME: 处理大数字的效率问题

def process_user_data(users):
    # 硬编码密钥 - 安全问题
    api_key = "sk-1234567890abcdef"
    
    results = []
    for user in users:
        # 调试打印语句
        print(f"处理用户: {user}")
        
        # 嵌套过深
        if user.get('active'):
            if user.get('age', 0) > 18:
                if user.get('country') == 'CN':
                    if user.get('subscription') == 'premium':
                        results.append(user)
    
    return results

# 长函数示例（超过50行）
def very_long_function():
    """这个函数故意写得很长，用于测试Qwen分析"""
    data = []
    for i in range(100):
        if i % 2 == 0:
            if i % 3 == 0:
                if i % 5 == 0:
                    data.append(f"{i} 能被2,3,5整除")
                else:
                    data.append(f"{i} 能被2,3整除")
            else:
                data.append(f"{i} 能被2整除")
        else:
            if i % 3 == 0:
                data.append(f"{i} 能被3整除")
            else:
                data.append(f"{i} 不能被2或3整除")
    
    # 更多处理...
    processed = []
    for item in data:
        processed.append(item.upper())
    
    filtered = []
    for item in processed:
        if '整除' in item:
            filtered.append(item)
    
    return filtered

if __name__ == "__main__":
    print(calculate_fibonacci(10))
    print(process_user_data([{'active': True, 'age': 25, 'country': 'CN', 'subscription': 'premium'}]))