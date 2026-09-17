import ast
import re
from typing import List
from .models import FileInfo, FileMetrics

def analyze_python_ast(source: str, metrics: FileMetrics):
    try:
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                metrics.num_functions += 1
            elif isinstance(node, ast.ClassDef):
                metrics.num_classes += 1
    except SyntaxError:
        pass

def analyze_metrics(files: List[FileInfo]) -> None:
    for f in files:
        if f.is_binary:
            continue

        metrics = FileMetrics()
        
        try:
            with open(f.path, 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()
        except Exception:
            continue

        metrics.code_lines = 0
        metrics.blank_lines = 0
        metrics.comment_lines = 0
        
        source_text = "".join(lines)

        for line in lines:
            line_len = len(line.rstrip('\n'))
            if line_len > metrics.longest_line:
                metrics.longest_line = line_len

            stripped = line.strip()
            if not stripped:
                metrics.blank_lines += 1
                continue
            
            # Very basic comment heuristic
            if stripped.startswith('#') or stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
                metrics.comment_lines += 1
            else:
                metrics.code_lines += 1
                
                # Heuristic nesting
                leading_spaces = len(line) - len(line.lstrip(' '))
                leading_tabs = len(line) - len(line.lstrip('\t'))
                # Assume 4 spaces = 1 depth, 1 tab = 1 depth
                depth = max(leading_spaces // 4, leading_tabs)
                if depth > metrics.max_nesting:
                    metrics.max_nesting = depth

        if f.extension == '.py':
            analyze_python_ast(source_text, metrics)
        else:
            # Heuristic function/class counts for non-Python
            for line in lines:
                stripped = line.strip()
                if re.match(r'^(public\s+|private\s+|protected\s+)?(class|struct)\s+\w+', stripped):
                    metrics.num_classes += 1
                elif re.match(r'^(public\s+|private\s+|protected\s+)?(static\s+)?\w+\s+\w+\s*\(', stripped) and not stripped.endswith(';'):
                    metrics.num_functions += 1
                elif re.match(r'^(function|func|def)\s+\w+', stripped):
                    metrics.num_functions += 1

        f.metrics = metrics


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
                complexity = len(re.findall(r'\b(if|elif|for|while|and|or|except|with)\b', body))
                if complexity > max_complexity:
                    max_complexity = complexity
                    god_func_name = name
                    god_func_file = f.relative_path
                    
        elif f.language == "JavaScript":
            funcs = re.finditer(r'function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(.*?\)\s*\{([\s\S]*?)(?=(?:function |\Z))', f.content)
            for m in funcs:
                name = m.group(1)
                body = m.group(2)
                complexity = len(re.findall(r'\b(if|else if|for|while|&&|\|\||catch|switch)\b', body))
                if complexity > max_complexity:
                    max_complexity = complexity
                    god_func_name = name
                    god_func_file = f.relative_path

    if max_complexity > 10:
        return f"{god_func_name} in {god_func_file} (Complexity: {max_complexity})"
    return ""
