import sys
import re

with open("repodoctor/metrics.py", "r", encoding="utf-8") as f:
    c = f.read()

god_func = """

def find_god_function(files) -> str:
    max_complexity = 0
    god_func_name = ""
    god_func_file = ""
    
    for f in files:
        if f.language == "Python":
            funcs = re.finditer(r'^def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(.*?\):([\s\S]*?)(?=(?:^def |\Z))', f.content, re.MULTILINE)
            for m in funcs:
                name = m.group(1)
                body = m.group(2)
                complexity = len(re.findall(r'\\b(if|elif|for|while|and|or|except|with)\\b', body))
                if complexity > max_complexity:
                    max_complexity = complexity
                    god_func_name = name
                    god_func_file = f.relative_path
                    
        elif f.language == "JavaScript":
            funcs = re.finditer(r'function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(.*?\)\s*\\{([\s\S]*?)(?=(?:function |\Z))', f.content)
            for m in funcs:
                name = m.group(1)
                body = m.group(2)
                complexity = len(re.findall(r'\\b(if|else if|for|while|&&|\\|\\||catch|switch)\\b', body))
                if complexity > max_complexity:
                    max_complexity = complexity
                    god_func_name = name
                    god_func_file = f.relative_path

    if max_complexity > 10:
        return f"{god_func_name} in {god_func_file} (Complexity: {max_complexity})"
    return ""
"""
c = c + god_func

with open("repodoctor/metrics.py", "w", encoding="utf-8") as f:
    f.write(c)
print("God function profiler injected")
