import sys

with open("repodoctor/__main__.py", "r", encoding="utf-8") as f:
    c = f.read()

# 1. Remove graph from bottom loop
c = c.replace("""        if getattr(args, "graph", False):
            from .graph import generate_graph
            print(generate_graph(res["files"]))""", "")

# 2. Add graph generation to process_single_repo
graph_logic = """        if getattr(args, "graph", False):
            from .graph import generate_graph
            graph_output = generate_graph(files)
            terminal_report += "\\n" + graph_output + "\\n"
            
    return {"""

c = c.replace("    return {", graph_logic)

with open("repodoctor/__main__.py", "w", encoding="utf-8") as f:
    f.write(c)

print("Moved graph to process_single_repo")
