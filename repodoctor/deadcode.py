import re

def find_dead_code(files) -> list:
    """
    Scans files for dead code (declared but never used).
    Returns a list of strings describing dead code found.
    """
    dead_code_issues = []
    
    # 1. Collect all declarations
    declared_funcs = {}
    for f in files:
        if f.language == "Python":
            # Match 'def func_name('
            matches = re.finditer(r'^def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', f.content, re.MULTILINE)
            for m in matches:
                name = m.group(1)
                # Ignore dunders
                if not (name.startswith('__') and name.endswith('__')):
                    declared_funcs[name] = f.relative_path
        elif f.language == "JavaScript":
            matches = re.finditer(r'^function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', f.content, re.MULTILINE)
            for m in matches:
                declared_funcs[m.group(1)] = f.relative_path
                
    # 2. Scan all files for usages
    if declared_funcs:
        used_funcs = set()
        for f in files:
            # simple word boundary regex
            words = set(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', f.content))
            # If a word exists in the file, and it's not the declaration line?
            # Actually, a simpler heuristic: if it appears MORE THAN ONCE across the entire project, it's used.
            # If it appears EXACTLY ONCE, it's dead code!
            # Let's count global occurrences!
            pass
            
    # Better heuristic: global token counting
    token_counts = {}
    for f in files:
        tokens = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', f.content)
        for t in tokens:
            token_counts[t] = token_counts.get(t, 0) + 1
            
    for name, path in declared_funcs.items():
        if token_counts.get(name, 0) == 1:
            dead_code_issues.append(f"💀 {path}: '{name}' is declared but never called globally!")
            
    return dead_code_issues
