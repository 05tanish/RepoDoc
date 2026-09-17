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
    file_keys = sorted(graph.keys())
    for i, file_path in enumerate(file_keys):
        deps = sorted(set(graph[file_path]))
        if not deps:
            continue

        is_last_file = (i == len(file_keys) - 1)
        file_prefix = "└── " if is_last_file else "├── "
        output.append(f"{file_prefix}{file_path}")

        for j, d in enumerate(deps):
            is_last_dep = (j == len(deps) - 1)
            dep_prefix = "    " if is_last_file else "│   "
            dep_prefix += "└── " if is_last_dep else "├── "
            output.append(f"{dep_prefix}{d}")

    return "\n".join(output)
