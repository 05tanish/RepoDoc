import re
import os

def generate_docs(files, root_path):
    """
    Parses files for functions and classes and generates markdown documentation.
    """
    docs_dir = os.path.join(root_path, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    
    docs_content = ["# API Reference\n"]
    
    for f in files:
        if f.language == "Python":
            # Very basic parser
            funcs = re.findall(r'^def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\):', f.content, re.MULTILINE)
            if funcs:
                docs_content.append(f"## `{f.relative_path}`")
                for name, params in funcs:
                    docs_content.append(f"- **`{name}({params})`**")
                docs_content.append("")
        elif f.language == "JavaScript":
            funcs = re.findall(r'function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)', f.content)
            if funcs:
                docs_content.append(f"## `{f.relative_path}`")
                for name, params in funcs:
                    docs_content.append(f"- **`{name}({params})`**")
                docs_content.append("")
                
    with open(os.path.join(docs_dir, "api_reference.md"), "w", encoding="utf-8") as out:
        out.write("\n".join(docs_content))
        
    return os.path.join(docs_dir, "api_reference.md")
