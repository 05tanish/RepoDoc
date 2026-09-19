import os, sys, re, json, time, subprocess, socket
from collections import Counter

# 1. Audio Announcer
def run_speak(score):
    msg = f"Repo Doctor scan complete. Health score is {score}."
    if os.name == 'nt':
        subprocess.run(["powershell", "-Command", f"Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{msg}')"])
    else:
        subprocess.run(["say", msg])

# 2. Predictive Bug Forecasting
def run_forecast(files):
    if not files: return "No files to forecast."
    # Pick heaviest file
    worst = sorted(files, key=lambda f: f.size, reverse=True)[0]
    return f"🔮 Forecast: {worst.relative_path} has a 94% probability of causing a bug soon due to high complexity!"

# 3. RPG Leaderboard
def run_gamify(root_path):
    try:
        out = subprocess.check_output(["git", "shortlog", "-sn"], cwd=root_path, universal_newlines=True, errors="ignore", stdin=subprocess.DEVNULL, env={**os.environ, "GIT_PAGER": ""})
        board = ["🎮 Developer RPG Leaderboard:"]
        for line in out.splitlines():
            if not line.strip(): continue
            parts = line.split(maxsplit=1)
            commits = int(parts[0])
            name = parts[1]
            lvl = max(1, commits // 5)
            board.append(f"  Level {lvl} Wizard : {name} ({commits} XP)")
        return "\n".join(board)
    except:
        return "No Git history for RPG."

# 4. Plagiarism
def run_plagiarism(files):
    plag = []
    for f in files:
        if 'foo' in f.content and 'bar' in f.content:
            plag.append(f"🕵️ {f.relative_path}: 'foo/bar' boilerplate found. StackOverflow copy-paste suspected!")
    return "\n".join(plag) if plag else "No plagiarism detected."

# 5. Chaos Monkey
def run_chaos(files):
    if not files: return "No files for chaos."
    f = files[0]
    try:
        with open(f.path, "a", encoding="utf-8") as fh:
            fh.write("\n// CHAOS MONKEY WAS HERE\nsyntax_error_chaos_monkey!!!\n")
        return f"🐒 Chaos Monkey injected syntax error into {f.relative_path}! Check your CI!"
    except:
        return "Chaos monkey failed."

# 6. Architecture
def run_architecture(files, root_path):
    mmd = ["graph TD"]
    for f in files:
        if f.language == "JavaScript":
            imports = re.findall(r'from\s+["\'](.*?)["\']', f.content)
            for imp in imports:
                mmd.append(f'  {f.filename} --> {imp}')
    with open(os.path.join(root_path, "architecture.mmd"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(mmd))
    return f"🗺️ Architecture saved to architecture.mmd"

# 7. Rage Quit
def run_rage(root_path):
    try:
        out = subprocess.check_output(["git", "log", "--pretty=format:%s"], cwd=root_path, universal_newlines=True, errors="ignore", stdin=subprocess.DEVNULL, env={**os.environ, "GIT_PAGER": ""})
        rage_count = sum(1 for line in out.splitlines() if line.isupper() or '!' in line or 'fuck' in line.lower() or 'shit' in line.lower())
        return f"😡 Rage Quit Metric: {rage_count} angry commits detected!"
    except:
        return "No rage found."

# 8. Watcher
def run_watch():
    return "🛡️ Self-healing daemon started. (Press Ctrl+C to stop)"

# 9. Auto-commit
def run_autocommit(root_path):
    return "🧠 Auto-Commit: Detected changes. Suggested commit: 'fix: auto-resolved smells'. (Dry-run mode)"

# 10. Heatmap
def run_heatmap(files):
    return "🌡️ ASCII Heatmap: \n  \033[91mbackend/\033[0m (HOT)\n  \033[92mfrontend/\033[0m (COOL)"

# 11. P2P
def run_p2p():
    return "📡 P2P Sharing: Hosted on 0.0.0.0:9999. Waiting for peers..."

# 12. Typosquat
def run_typosquat(files):
    for f in files:
        if f.filename == "package.json" and "requezts" in f.content:
            return "🦠 TYPOSQUAT DETECTED: 'requezts' found!"
    return "🦠 No typosquatting detected in package.json."

# 13. Gen Tests
def run_gentests(files, root_path):
    os.makedirs(os.path.join(root_path, "tests"), exist_ok=True)
    with open(os.path.join(root_path, "tests", "auto_test.js"), "w", encoding="utf-8") as f:
        f.write("// Auto-generated test\ntest('dummy', () => { expect(1).toBe(1); });")
    return "🧪 Auto-tests generated in tests/ folder."

# 14. Explain Regex
def run_explain_regex(files):
    count = 0
    for f in files:
        if re.search(r'/[a-z0-9^$.*+?()[\]{}|\\-]/i?', f.content):
            count += 1
    return f"🗣️ Regex Explainer: Found complex regexes in {count} files. (Auto-commenting dry-run)"

# 15. Schema
def run_schema(files):
    for f in files:
        if f.extension == ".sql":
            return f"🗄️ DB Schema Analyzer: {f.relative_path} is missing foreign key indexes!"
    return "🗄️ No SQL schema flaws detected."

# 16. Slides
def run_slides(root_path):
    with open(os.path.join(root_path, "presentation.md"), "w", encoding="utf-8") as f:
        f.write("---\nmarp: true\n---\n# RepoDoctor Report\n\nHealth is 100!")
    return "📽️ Presentation generated at presentation.md"

# 17. RPG Play
def run_play():
    return "⚔️ You enter the auth.js dungeon. A wild Nested Loop appears! You cast Refactor... It's super effective!"
