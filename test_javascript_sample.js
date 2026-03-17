// TODO: 这是一个待办事项示例
// FIXME: 这是一个需要修复的问题示例

// 硬编码密码 - 安全问题
const password = "hardcoded123";
const apiKey = 'sk-1234567890abcdef';

// 使用var而不是let/const
var oldVariable = "should use let or const";

function veryLongFunction(param1, param2, param3, param4, param5) {
    // 控制台调试语句
    console.log("Debug: Processing param1", param1);
    console.info("Additional info");
    
    // 深层嵌套示例
    if (param1 > 0) {
        if (param2 > 0) {
            if (param3 > 0) {
                if (param4 > 0) {
                    if (param5 > 0) {
                        // 回调地狱示例
                        setTimeout(function() {
                            fetchData(function(data) {
                                processData(data, function(result) {
                                    console.log(result);
                                });
                            });
                        }, 1000);
                        
                        // 使用eval - 安全风险
                        eval("console.log('unsafe')");
                    }
                }
            }
        }
    }
    
    // 长行示例（超过120字符）
    const veryLongVariableName = "This is a very long line that exceeds the recommended maximum line length of 120 characters and should trigger a warning in the code quality analyzer";
    
    // Alert语句
    alert("This should be replaced with proper UI notification");
    
    return param1 + param2 + param3 + param4 + param5;
}

// 大型函数示例
function anotherLargeFunction() {
    // 这个函数故意写得很长，超过50行
    let result = [];
    for (let i = 0; i < 100; i++) {
        if (i % 2 === 0) {
            if (i % 3 === 0) {
                if (i % 5 === 0) {
                    result.push(`Number ${i} is divisible by 2, 3, and 5`);
                } else {
                    result.push(`Number ${i} is divisible by 2 and 3`);
                }
            } else {
                result.push(`Number ${i} is divisible by 2`);
            }
        } else {
            if (i % 3 === 0) {
                result.push(`Number ${i} is divisible by 3`);
            } else {
                result.push(`Number ${i} is not divisible by 2 or 3`);
            }
        }
    }
    
    // 更多代码行...
    let processedResult = [];
    for (let item of result) {
        let processedItem = item.toUpperCase();
        processedResult.push(processedItem);
    }
    
    let finalResult = [];
    for (let item of processedResult) {
        if (item.includes("DIVISIBLE")) {
            finalResult.push(item);
        }
    }
    
    return finalResult;
}

// 使用var的示例
function exampleWithVar() {
    var x = 10;
    if (x > 5) {
        var y = 20; // 变量提升问题
        console.log(y);
    }
    console.log(y); // 这里可以访问y，但可能不是预期的行为
}

// XXX: 另一个标记示例
if (typeof window !== 'undefined') {
    console.warn("Running in browser environment");
}

module.exports = {
    veryLongFunction,
    anotherLargeFunction,
    exampleWithVar
};