import sys
import re

with open("repodoctor/git.py", "r", encoding="utf-8") as f:
    git_c = f.read()

bus_inject = """            # Get top hotspot
            hotspot_output = subprocess.check_output(
                ["git", "log", "--pretty=format:", "--name-only"], 
                cwd=path, universal_newlines=True, errors="ignore"
            )
            files = [line.strip() for line in hotspot_output.splitlines() if line.strip()]
            if files:
                top_file, edits = collections.Counter(files).most_common(1)[0]
                info.hotspot = f"{top_file} ({edits} edits)"
                
            # BUS FACTOR
            try:
                if files:
                    bus_files = []
                    top_files_to_check = [f for f, _ in collections.Counter(files).most_common(5)]
                    for tf in top_files_to_check:
                        author_output = subprocess.check_output(
                            ["git", "shortlog", "-sn", "--", tf],
                            cwd=path, universal_newlines=True, errors="ignore"
                        )
                        authors = [line for line in author_output.splitlines() if line.strip()]
                        if len(authors) == 1:
                            bus_files.append(tf)
                    if bus_files:
                        info.bus_factor = bus_files
            except Exception:
                pass
"""

git_c = git_c.replace("""            # Get top hotspot
            hotspot_output = subprocess.check_output(
                ["git", "log", "--pretty=format:", "--name-only"], 
                cwd=path, universal_newlines=True, errors="ignore"
            )
            files = [line.strip() for line in hotspot_output.splitlines() if line.strip()]
            if files:
                top_file, edits = collections.Counter(files).most_common(1)[0]
                info.hotspot = f"{top_file} ({edits} edits)" """, bus_inject)

with open("repodoctor/git.py", "w", encoding="utf-8") as f:
    f.write(git_c)
print("Git bus factor patched")
