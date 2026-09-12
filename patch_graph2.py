import sys
import re

with open("repodoctor/__main__.py", "r", encoding="utf-8") as f:
    c = f.read()

bad_block = """        llm_report = prompt_chunk

        if getattr(args, "graph", False):
            from .graph import generate_graph
            graph_output = generate_graph(files)
            terminal_report += "\\n" + graph_output + "\\n"
            
    return {"""

good_block = """        llm_report = prompt_chunk

    if getattr(args, "graph", False):
        from .graph import generate_graph
        graph_output = generate_graph(files)
        terminal_report += "\\n" + graph_output + "\\n"
            
    return {"""

c = c.replace(bad_block, good_block)

with open("repodoctor/__main__.py", "w", encoding="utf-8") as f:
    f.write(c)

print("Fixed indentation!")
