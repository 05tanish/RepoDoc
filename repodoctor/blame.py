import subprocess
import os

def get_git_blame(filepath: str, line_num: int) -> str:
    """
    Runs git blame for a specific line in a file and returns the author.
    """
    try:
        if not os.path.exists(filepath):
            return "Unknown"
        out = subprocess.check_output(
            ["git", "blame", "-L", f"{line_num},{line_num}", "--", filepath],
            universal_newlines=True, errors="ignore", stderr=subprocess.DEVNULL
        )
        # Output format: ^hash (Author Name 2023-01-01...)
        if out and '(' in out:
            author_part = out.split('(', 1)[1]
            # It's tricky to parse author name perfectly because it can have spaces, but dates usually start with 20
            # Let's just grab the first word or everything before the first number
            import re
            match = re.search(r'([^\d]+)\s+\d{4}-', author_part)
            if match:
                return match.group(1).strip()
            else:
                return author_part.split()[0]
    except Exception:
        pass
    return "Unknown"
