import sys

with open("repodoctor/cli.py", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace('parser.add_argument("--interactive"', 
'''parser.add_argument("--serve", action="store_true", help="Host live web dashboard on localhost:8080")
    parser.add_argument("--blame", action="store_true", help="Run git blame on code smells")
    parser.add_argument("--docs", action="store_true", help="Generate API documentation")
    parser.add_argument("--legal", action="store_true", help="Scan for legal and license risks")
    parser.add_argument("--interactive"''')

with open("repodoctor/cli.py", "w", encoding="utf-8") as f:
    f.write(c)

with open("repodoctor/__main__.py", "r", encoding="utf-8") as f:
    m = f.read()

serve_inject = """        if getattr(args, "serve", False) and html_outputs:
            # write HTML somewhere
            import os
            from .serve import start_server
            with open("live_report.html", "w", encoding="utf-8") as out:
                out.write(html_outputs[-1])
            import repodoctor.serve
            repodoctor.serve.ReportHandler.report_html = html_outputs[-1]
            start_server(8080)
            print("Press Ctrl+C to stop the server.")
            import time
            try:
                while True: time.sleep(1)
            except KeyboardInterrupt:
                sys.exit(0)
"""
m = m.replace("    if getattr(args, \"export_prompt\"", serve_inject + "    if getattr(args, \"export_prompt\"")

docs_inject = """        if getattr(args, "docs", False):
            from .docsgen import generate_docs
            doc_path = generate_docs(files, root_path)
            terminal_report += f"\\n📚 Documentation generated at: {doc_path}\\n"
            
        if getattr(args, "legal", False):
            from .legal import scan_legal
            legal_warns = scan_legal(files)
            if legal_warns:
                terminal_report += "\\n" + "\\n".join(legal_warns) + "\\n"
"""
m = m.replace("        if getattr(args, \"graph\", False):", docs_inject + "        if getattr(args, \"graph\", False):")

with open("repodoctor/__main__.py", "w", encoding="utf-8") as f:
    f.write(m)

print("Main and CLI patched for v4")
