import sys
import re

with open("repodoctor/security.py", "r", encoding="utf-8") as f:
    sec_c = f.read()

# Replace the simple SECRET_PATTERNS with enterprise ones
old_patterns = """SECRET_PATTERNS = [
    r"api_key\\s*=\\s*['\"][a-zA-Z0-9]+['\"]",
    r"password\\s*=\\s*['\"][^'\"]+['\"]",
    r"secret\\s*=\\s*['\"][^'\"]+['\"]",
]"""

new_patterns = """SECRET_PATTERNS = [
    r"(?i)api_key\s*=\s*['\"][a-zA-Z0-9]+['\"]",
    r"(?i)password\s*=\s*['\"][^'\"]+['\"]",
    r"(?i)secret\s*=\s*['\"][^'\"]+['\"]",
    r"AKIA[0-9A-Z]{16}",                             # AWS Access Key ID
    r"ghp_[a-zA-Z0-9]{36}",                          # GitHub Personal Access Token
    r"sk_live_[a-zA-Z0-9]{24}",                      # Stripe Secret Key
    r"xoxb-[0-9]{10,13}-[a-zA-Z0-9]*",               # Slack Bot Token
    r"discord\.com/api/webhooks/[0-9]+/[a-zA-Z0-9_-]+", # Discord Webhook
]"""

sec_c = sec_c.replace(old_patterns, new_patterns)

with open("repodoctor/security.py", "w", encoding="utf-8") as f:
    f.write(sec_c)
print("Security updated")
