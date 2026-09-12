import os
import json
import re

def load_config(root_path: str):
    """
    Loads configuration from repodoctor.json or pyproject.toml in the root path.
    Returns a dictionary of arguments to override CLI defaults.
    """
    config = {}
    
    # Try repodoctor.json
    json_path = os.path.join(root_path, "repodoctor.json")
    if os.path.isfile(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                config.update(json.load(f))
        except Exception:
            pass

    # Try pyproject.toml [tool.repodoctor]
    toml_path = os.path.join(root_path, "pyproject.toml")
    if os.path.isfile(toml_path):
        try:
            with open(toml_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Extremely naive TOML parser for [tool.repodoctor] section
                match = re.search(r'\[tool\.repodoctor\](.*?)(?:^\[|$)', content, re.MULTILINE | re.DOTALL)
                if match:
                    section = match.group(1)
                    for line in section.splitlines():
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if "=" in line:
                            key, val = line.split("=", 1)
                            key = key.strip()
                            val = val.strip()
                            # Parse boolean
                            if val.lower() == "true": val = True
                            elif val.lower() == "false": val = False
                            # Parse int
                            elif val.isdigit(): val = int(val)
                            # Parse string
                            elif val.startswith('"') and val.endswith('"'): val = val[1:-1]
                            elif val.startswith("'") and val.endswith("'"): val = val[1:-1]
                            config[key] = val
        except Exception:
            pass

    return config
