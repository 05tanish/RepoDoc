import re
import os

from typing import Tuple

def apply_fixes(file_path: str, content: str, language: str) -> Tuple[str, bool]:
    """
    Applies safe automatic fixes to the file content.
    Returns the (modified content, was_modified).
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

    was_saved = False
    if modified and content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            was_saved = True
        except Exception:
            pass

    return content, was_saved
