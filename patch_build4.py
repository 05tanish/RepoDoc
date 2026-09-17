import sys

with open("build_single_file.py", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace(
    "'ai.py',", 
    "'serve.py',\n    'blame.py',\n    'docsgen.py',\n    'legal.py',\n    'ai.py',"
)

with open("build_single_file.py", "w", encoding="utf-8") as f:
    f.write(c)
print("Updated build script for v4")
