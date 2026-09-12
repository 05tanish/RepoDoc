import sys
import re

with open("build_single_file.py", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace(
    "'__main__.py'", 
    "'config.py',\n    'autofix.py',\n    'graph.py',\n    'linter.py',\n    '__main__.py'"
)

with open("build_single_file.py", "w", encoding="utf-8") as f:
    f.write(c)
print("Updated builder")
