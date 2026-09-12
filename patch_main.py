import sys
import re

with open("repodoctor/__main__.py", "r", encoding="utf-8") as f:
    main = f.read()

# 1. Inject Config and Init-CI at the top of main()
config_injection = """    args = parse_args()

    # Load native config if exists
    from .config import load_config
    for rp in args.path:
        config = load_config(rp)
        for k, v in config.items():
            if hasattr(args, k) and getattr(args, k) == getattr(args.__class__, k, None): # Only override if default? Let's just override loosely
                pass # Wait, simpler: just dict update
        for k, v in config.items():
            setattr(args, k, v)

    # Init CI/CD
    if getattr(args, "init_ci", False):
        import os
        for rp in args.path:
            wf_dir = os.path.join(rp, ".github", "workflows")
            os.makedirs(wf_dir, exist_ok=True)
            wf_path = os.path.join(wf_dir, "repodoctor.yml")
            with open(wf_path, "w", encoding="utf-8") as f:
                f.write('''name: RepoDoctor Health Check
on: [push, pull_request]
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - name: Install RepoDoctor
        run: pip install repodoctor-cli
      - name: Run RepoDoctor
        run: repodoctor . --fail-under 70
''')
            print(f"✔ CI/CD pipeline generated at {wf_path}")
        sys.exit(0)
"""

main = main.replace("    args = parse_args()", config_injection)

# 2. Inject Autofix inside process_single_repo loop
autofix_inject = """            f = FileInfo(
                path=filepath,
                relative_path=rel_path,
                size=os.path.getsize(filepath),
                lines=lines
            )
            f.content = content
            f.language = detect_language(filepath)
            
            # AUTO FIX ENGINE
            if getattr(args, "fix", False):
                from .autofix import apply_fixes
                f.content = apply_fixes(filepath, f.content, f.language)
"""

main = re.sub(r'            f\.language = detect_language\(filepath\)', autofix_inject, main)

# 3. Inject Graph at the end
graph_inject = """        if res["html_report"] is not None:
            html_outputs.append(res["html_report"])
        if res["llm_report"] is not None:
            llm_outputs.append(res["llm_report"])
            
        if getattr(args, "graph", False):
            from .graph import generate_graph
            print(generate_graph(res["files"]))
"""

main = main.replace("""        if res["html_report"] is not None:
            html_outputs.append(res["html_report"])
        if res["llm_report"] is not None:
            llm_outputs.append(res["llm_report"])""", graph_inject)


with open("repodoctor/__main__.py", "w", encoding="utf-8") as f:
    f.write(main)

print("Injected into __main__.py!")
