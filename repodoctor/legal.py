import re
import os

def scan_legal(files) -> list:
    """
    Scans files for dangerous licenses like GPL.
    Returns a list of warning strings.
    """
    warnings = []
    
    for f in files:
        if f.filename == "package.json":
            match = re.search(r'"license"\s*:\s*"([^"]+)"', f.content, re.IGNORECASE)
            if match:
                lic = match.group(1).upper()
                if "GPL" in lic and "LGPL" not in lic:
                    warnings.append(f"⚖️ {f.relative_path}: Declares {lic} license (Copyleft risk!)")
                    
        elif f.filename == "LICENSE" or f.filename.startswith("LICENSE."):
            if "GNU GENERAL PUBLIC LICENSE" in f.content.upper():
                warnings.append(f"⚖️ {f.relative_path}: GPL license detected in file contents (Copyleft risk!)")
                
    return warnings
