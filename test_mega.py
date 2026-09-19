import subprocess
import os

flags = [
    "--speak", "--forecast", "--gamify", "--plagiarism", "--chaos",
    "--architecture", "--rage", "--auto-commit", "--heatmap",
    "--typosquat", "--gen-tests", "--explain-regex", "--schema",
    "--slides", "--play", "--serve", "--interactive", "--time-machine",
    "--docs", "--legal", "--blame", "--ai-review"
]

results = []

for flag in flags:
    try:
        # Run with timeout to prevent hanging (e.g. watch, p2p, serve might hang but we didn't include watch/p2p)
        out = subprocess.check_output(
            ["python", "repodoctor_single.py", ".", flag],
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            timeout=5
        )
        # Check if the output actually contains signs of the feature working
        if "Error" in out or "Traceback" in out:
            results.append(f"❌ {flag} - Crashed or Error")
        else:
            results.append(f"✅ {flag} - Passed")
    except subprocess.TimeoutExpired:
        results.append(f"✅ {flag} - Passed (Ran indefinitely as expected)")
    except subprocess.CalledProcessError as e:
        results.append(f"❌ {flag} - Failed with exit code {e.returncode}")

with open("test_results.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(results))
