import sys

with open("repodoctor/report.py", "r", encoding="utf-8") as f:
    rep_c = f.read()

bus_inject = """    print(c("GIT", "36;1"))
    print(c("─" * 60, "90"))
    if data.git.error:
        print(c(f"  {data.git.error}", "90"))
    else:
        print(f"{c('Branch:', '90'):<24} {c(data.git.branch, '92')}")
        print(f"{c('Uncommitted changes:', '90'):<24} {c(str(data.git.uncommitted), '93' if data.git.uncommitted > 0 else '92')}")
        print(f"{c('Commits:', '90'):<24} {data.git.commits}")
        if data.git.top_contributor:
            print(f"{c('Top Contributor:', '90'):<24} {c(data.git.top_contributor, '96')}")
        if data.git.hotspot:
            print(f"{c('🔥 Hotspot file:', '90'):<24} {c(data.git.hotspot, '91')}")
        if data.git.bus_factor:
            bus_str = ', '.join(data.git.bus_factor[:3]) + ('...' if len(data.git.bus_factor) > 3 else '')
            print(f"{c('🚌 Bus Factor Risks:', '90'):<24} {c(bus_str, '91')}")
"""

# Replace the GIT section in print_terminal_report
rep_c = rep_c.replace("""    print(c("GIT", "36;1"))
    print(c("─" * 60, "90"))
    if data.git.error:
        print(c(f"  {data.git.error}", "90"))
    else:
        print(f"{c('Branch:', '90'):<24} {c(data.git.branch, '92')}")
        print(f"{c('Uncommitted changes:', '90'):<24} {c(str(data.git.uncommitted), '93' if data.git.uncommitted > 0 else '92')}")
        print(f"{c('Commits:', '90'):<24} {data.git.commits}")
        if data.git.top_contributor:
            print(f"{c('Top Contributor:', '90'):<24} {c(data.git.top_contributor, '96')}")
        if data.git.hotspot:
            print(f"{c('🔥 Hotspot file:', '90'):<24} {c(data.git.hotspot, '91')}")""", bus_inject)

with open("repodoctor/report.py", "w", encoding="utf-8") as f:
    f.write(rep_c)
print("Report updated")
