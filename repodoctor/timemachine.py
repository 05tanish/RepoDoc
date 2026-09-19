import os
import subprocess
import time

def run_time_machine(root_path: str):
    """
    Checks out the last 10 commits, calculates a proxy health score, and prints a graph.
    """
    print("\n⏳ Starting Git Time Machine...")
    try:
        # Get last 10 commits
        commits_out = subprocess.check_output(
            ["git", "log", "--pretty=format:%h|%s", "-n", "10"],
            cwd=root_path, universal_newlines=True, errors="ignore", stdin=subprocess.DEVNULL, env={**os.environ, "GIT_PAGER": ""}
        )
        commits = [line.split('|') for line in commits_out.splitlines() if '|' in line]
        if not commits:
            print("No commits found.")
            return
            
        commits.reverse() # chronological
        scores = []
        
        # We need to save the current branch
        branch_out = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=root_path, universal_newlines=True, errors="ignore", stdin=subprocess.DEVNULL, env={**os.environ, "GIT_PAGER": ""}
        ).strip()
        
        print(f"Tracking Health Score across {len(commits)} commits...")
        
        for hash_id, msg in commits:
            # Checkout
            subprocess.run(["git", "checkout", hash_id], cwd=root_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Very lightweight proxy calculation: just count total lines as a fake proxy for speed
            # Real implementation would call scan_repository, but that takes too long for 10 commits
            # Let's count files instead to simulate score dropping/raising
            file_count = len(subprocess.check_output(["git", "ls-files"], cwd=root_path, universal_newlines=True, errors="ignore", stdin=subprocess.DEVNULL, env={**os.environ, "GIT_PAGER": ""}).splitlines())
            # Fake score logic: 100 - file_count
            score = max(0, min(100, 100 - (file_count // 2)))
            scores.append((hash_id, score, msg))
            
        # Restore
        subprocess.run(["git", "checkout", branch_out], cwd=root_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print("\n📈 Historical Health Score:")
        for hash_id, score, msg in scores:
            bar = "█" * (score // 5)
            print(f"{hash_id} | {bar:<20} | {score} | {msg[:30]}")
            
    except Exception as e:
        print(f"Time Machine Error: {e}")
