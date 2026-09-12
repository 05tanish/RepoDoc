import re
import os

def apply_fixes(file_path: str, content: str, language: str) -> str:
    """
    Applies safe automatic fixes to the file content.
    Returns the modified content, or original content if no changes.
    """
    original_content = content
    modified = False

    # Fix: Trailing whitespace
    if re.search(r'[ \t]+$', content, re.MULTILINE):
        content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)
        modified = True
        
    # Fix: Missing EOF newline
    if content and not content.endswith('\n'):
        content += '\n'
        modified = True
        
    # Fix: Missing 'use strict' in JS (only if not already there and file has logic)
    if language == "JavaScript" and not re.search(r'["\']use strict["\']', content) and len(content.strip()) > 20:
        content = '"use strict";\n\n' + content
        modified = True

    if modified and content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception:
            pass
            
    return content
