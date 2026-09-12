import re
import os
from collections import defaultdict

def generate_graph(files) -> str:
    """
    Scans files for import statements and builds a lightweight dependency graph.
    Returns an ASCII string representation of the graph.
    """
    graph = defaultdict(list)
    
    for f in files:
        if f.language == "Python":
            # Very naive Python import parser
            imports = re.findall(r'^import ([a-zA-Z0-9_\.]+)', f.content, re.MULTILINE)
            from_imports = re.findall(r'^from ([a-zA-Z0-9_\.]+) import', f.content, re.MULTILINE)
            for imp in imports + from_imports:
                graph[f.relative_path].append(imp)
        elif f.language == "JavaScript":
            # Very naive JS import parser
            imports = re.findall(r'import .*? from ["\'](.*?)["\']', f.content)
            requires = re.findall(r'require\(["\'](.*?)["\']\)', f.content)
            for imp in imports + requires:
                graph[f.relative_path].append(imp)
                
    if not graph:
        return "No local dependencies detected."
        
    output = ["\nASCII Dependency Graph:"]
    for file_path, deps in graph.items():
        if deps:
            output.append(f"├── {file_path}")
            for d in deps:
                output.append(f"│   └── {d}")
                
    return "\n".join(output)
