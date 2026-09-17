import re
from typing import List, Tuple
from .models import FileInfo, SecurityFinding

PATTERNS = [
    # (Regex, Category, Confidence, Explanation)
    (re.compile(r'(?i)(?:api_?key|secret|token|password)[\s:=]+[\'"]([A-Za-z0-9_\-]{16,})[\'"]'), "API Key or Token", "HIGH", "A variable name suggests an API key or token was hardcoded."),
    (re.compile(r'-----BEGIN [A-Z]+ PRIVATE KEY-----'), "Private Key", "HIGH", "A private cryptographic key is present."),
    (re.compile(r'https?://[a-zA-Z0-9_\-]+:[a-zA-Z0-9_\-]+@[a-zA-Z0-9_\-\.]+'), "Credential URL", "HIGH", "A URL contains embedded basic authentication credentials."),
    (re.compile(r'(sk-[a-zA-Z0-9]{20,})'), "Potential API Key", "HIGH", "Pattern matches common cloud API keys (e.g., sk-...)."),
    (re.compile(r'(AKIA[0-9A-Z]{16})'), "AWS Access Key", "CRITICAL", "AWS Access Key ID exposed."),
    (re.compile(r'(sk_(live|test)_[0-9a-zA-Z]{24,})'), "Stripe Secret", "CRITICAL", "Stripe Secret Key exposed."),
    (re.compile(r'(gh[pousr]_[A-Za-z0-9_]{36,})'), "GitHub PAT", "CRITICAL", "GitHub Personal Access Token exposed."),
    (re.compile(r'(xox[baprs]-[0-9]+-[a-zA-Z0-9]+)'), "Slack Token", "CRITICAL", "Slack API Token exposed."),
    (re.compile(r'(discord\.com/api/webhooks/[0-9]+/[a-zA-Z0-9_-]+)'), "Discord Webhook", "CRITICAL", "Discord Webhook exposed.")
]

def redact(value: str) -> str:
    if len(value) <= 5:
        return "***"
    return value[:3] + "..." + value[-2:]

def scan_security(files: List[FileInfo]) -> List[SecurityFinding]:
    findings = []

    for f in files:
        if f.is_binary:
            continue

        # Check .env
        if f.filename.startswith(".env"):
            findings.append(SecurityFinding(
                filepath=f.relative_path,
                line_number=0,
                category="Environment File",
                confidence="HIGH",
                explanation="An environment file (e.g., .env) is checked in. This often contains secrets.",
                redacted_value="N/A"
            ))

        try:
            with open(f.path, 'r', encoding='utf-8', errors='ignore') as file:
                for line_idx, line in enumerate(file):
                    for pattern, category, confidence, explanation in PATTERNS:
                        match = pattern.search(line)
                        if match:
                            # For private key header, the match is the whole header
                            val_to_redact = match.group(1) if len(match.groups()) > 0 else match.group(0)

                            findings.append(SecurityFinding(
                                filepath=f.relative_path,
                                line_number=line_idx + 1,
                                category=category,
                                confidence=confidence,
                                explanation=explanation,
                                redacted_value=redact(val_to_redact)
                            ))
        except Exception:
            pass

    return findings


def check_devops_security(filename: str, content: str):
    issues = []
    fname = filename.lower()
    
    if 'dockerfile' in fname:
        if not re.search(r'(?i)^USER\s+(?!root)[a-zA-Z0-9_]+', content, re.MULTILINE):
            issues.append(f"⚠️ {filename}: Container runs as root (missing explicit non-root USER instruction)")
            
    if 'docker-compose' in fname:
        if 'ports:' in content and '22:22' in content:
            issues.append(f"🚨 {filename}: SSH Port 22 is exposed!")
            
    return issues
