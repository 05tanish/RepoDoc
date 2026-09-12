import sys

with open("repodoctor/__main__.py", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace("        import os\n", "")

with open("repodoctor/__main__.py", "w", encoding="utf-8") as f:
    f.write(c)

print("Removed local os import")
