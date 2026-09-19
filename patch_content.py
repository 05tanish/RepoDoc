import sys
import re

with open("repodoctor/mega.py", "r", encoding="utf-8") as f:
    c = f.read()

def inject_content_loader(match):
    return 'try:\\n            with open(f.path, "r", encoding="utf-8", errors="ignore") as fh:\\n                f_content = fh.read()\\n        except:\\n            continue\\n        if \\'foo\\' in f_content and \\'bar\\' in f_content:'

# Wait, it's easier to just do a global replace of `f.content` to a helper function, or just inject a content read loop.
# I'll just write a quick script to replace `f.content` with `getattr(f, 'content', '')` NO wait, `f.content` is not set at all!

with open("repodoctor/mega.py", "w", encoding="utf-8") as f:
    # Plagiarism
    c = c.replace("if 'foo' in f.content and 'bar' in f.content:", "try: f_content = open(f.path, 'r', encoding='utf-8', errors='ignore').read()\n        except: continue\n        if 'foo' in f_content and 'bar' in f_content:")
    
    # Architecture
    c = c.replace("imports = re.findall(r'from\\s+[\"\\'](.*?)[\"\\']', f.content)", "try: f_content = open(f.path, 'r', encoding='utf-8', errors='ignore').read()\n            except: continue\n            imports = re.findall(r'from\\s+[\"\\'](.*?)[\"\\']', f_content)")
    
    # Typosquat
    c = c.replace("if f.filename == \"package.json\" and \"requezts\" in f.content:", "try: f_content = open(f.path, 'r', encoding='utf-8', errors='ignore').read()\n        except: continue\n        if f.filename == \"package.json\" and \"requezts\" in f_content:")
    
    # Gen Tests
    c = c.replace("funcs = re.findall(r'function\\s+([a-zA-Z_0-9]+)\\s*\\(', f.content)", "try: f_content = open(f.path, 'r', encoding='utf-8', errors='ignore').read()\n            except: continue\n            funcs = re.findall(r'function\\s+([a-zA-Z_0-9]+)\\s*\\(', f_content)")
    
    # Explain Regex
    c = c.replace("if re.search(r'/[a-z0-9^$.*+?()[\\]{}|\\\\-]/i?', f.content):", "try: f_content = open(f.path, 'r', encoding='utf-8', errors='ignore').read()\n        except: continue\n        if re.search(r'/[a-z0-9^$.*+?()[\\]{}|\\\\-]/i?', f_content):")
    
    f.write(c)

print("Fixed mega.py content reading")
