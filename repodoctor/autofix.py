import os
import re

def apply_fixes(files):
    fixed_count = 0
    for f in files:
        original = f.content
        content = f.content
        
        # 1. Strip trailing whitespace
        content = "\n".join(line.rstrip() for line in content.splitlines())
        
        # 2. Ensure EOF newline
        if content and not content.endswith('\n'):
            content += '\n'
            
        # 3. JS/TS specific fixes
        if f.language in ["JavaScript", "TypeScript"]:
            # Add use strict if missing
            if not re.search(r'^[\'"]use strict[\'"]', content, re.MULTILINE):
                content = '"use strict";\n' + content
                
            # Remove all console.log statements (clean up debugging)
            content = re.sub(r'^\s*console\.log\(.*?\);\s*$', '', content, flags=re.MULTILINE)
            
            # Convert var to let
            content = re.sub(r'\bvar\b', 'let', content)
            
        # 4. Python specific fixes
        elif f.language == "Python":
            # Remove empty pass blocks where possible, or just remove debugging print statements
            # Wait, removing print might be dangerous, let's just remove multiple blank lines
            content = re.sub(r'\n{3,}', '\n\n', content)
            
            # Fix bare excepts to except Exception:
            content = re.sub(r'^\s*except\s*:\s*$', 'except Exception:', content, flags=re.MULTILINE)
            
        if content != original:
            try:
                with open(f.path, 'w', encoding='utf-8') as out:
                    out.write(content)
                fixed_count += 1
            except Exception:
                pass
                
    return fixed_count
