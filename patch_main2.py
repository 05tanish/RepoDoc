import sys

with open("repodoctor/__main__.py", "r", encoding="utf-8") as f:
    c = f.read()

# 1. Inject Autofix after scan_repository
autofix_block = """    # 1. Scan files
    files = scan_repository(
        root_path,
        custom_ignores,
        parallel=use_parallel,
        show_animation=show_animation,
        progress_msg=f"Scanning files ({root_path})",
    )
    
    if getattr(args, "fix", False):
        from .autofix import apply_fixes
        from .languages import _detect_language_from_ext
        for f in files:
            lang = _detect_language_from_ext(f.extension)
            if lang in ["Unknown", "Binary"]:
                continue
            try:
                with open(f.path, 'r', encoding='utf-8') as fh:
                    content = fh.read()
                new_content = apply_fixes(f.path, content, lang)
            except Exception:
                pass
"""

c = c.replace("""    # 1. Scan files
    files = scan_repository(
        root_path,
        custom_ignores,
        parallel=use_parallel,
        show_animation=show_animation,
        progress_msg=f"Scanning files ({root_path})",
    )""", autofix_block)

# 2. Fix the graph generator to read files
c = c.replace("        graph_output = generate_graph(files)", """        # populate content for graph
        for f in files:
            try:
                with open(f.path, 'r', encoding='utf-8', errors='ignore') as fh:
                    f.content = fh.read()
            except Exception:
                f.content = ""
                
        graph_output = generate_graph(files)""")

with open("repodoctor/__main__.py", "w", encoding="utf-8") as f:
    f.write(c)

print("Fixed autofix and graph reading!")
