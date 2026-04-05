import os
import sys

# Dynamic root discovery
_current_dir = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = None
while True:
    if os.path.exists(os.path.join(_current_dir, 'core')):
        PROJECT_ROOT = _current_dir
        if PROJECT_ROOT not in sys.path:
            sys.path.insert(0, PROJECT_ROOT)
        break
    parent = os.path.dirname(_current_dir)
    if parent == _current_dir: # root reached
        break
    _current_dir = parent

import yaml
import json
from datetime import datetime, timedelta
from core.data_manager import load_data, _get_nested

SKILLS_DIR = os.path.join(PROJECT_ROOT, "skills") if PROJECT_ROOT else "skills"

def parse_skill_contract(skill_name):
    """Parse YAML frontmatter from SKILL.md."""
    skill_md_path = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
    if not os.path.exists(skill_md_path):
        return None
    
    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if content.startswith('---'):
            try:
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    return yaml.safe_load(parts[1])
            except Exception:
                pass
    return None

def is_populated(data_node):
    """Recursively check if a node has non-default clinical data."""
    if isinstance(data_node, dict):
        if "updated_at" in data_node:
            # Clinical leaf node: MUST have a non-empty timestamp to be populated
            return bool(data_node.get("updated_at"))
        # Container node: skip static metadata fields
        return any(is_populated(v) for k, v in data_node.items() if k not in ["unit", "scale", "insulin_type", "frequency", "risk_category"])
    if isinstance(data_node, list):
        return len(data_node) > 0
    # Scalar values (less common in clinical fields, but handled)
    return data_node not in [None, "", 0, 0.0]

def check_prerequisites(skill_name):
    """
    Validate SSOT paths exist and meet freshness constraints.
    Returns: (is_ready, warnings)
    """
    contract = parse_skill_contract(skill_name)
    if not contract:
        # If we have PROJECT_ROOT but still no contract, return True for flexibility
        return True, [] 
    
    data = load_data()
    warnings = []
    is_ready = True
    
    requires = contract.get('requires', {})
    ssot_reqs = requires.get('ssot', [])
    
    for req in ssot_reqs:
        path = req.get('path')
        freshness = req.get('freshness') # e.g., '1h', '7d'
        
        try:
            item = _get_nested(data, path)
            
            # Deep Check for population
            if not is_populated(item):
                is_ready = False
                warnings.append(f"MISSING: Required data '{path}' is not yet populated.")
                continue

            # Check freshness if applicable
            def get_timestamps(node):
                ts = []
                if isinstance(node, dict):
                    if "updated_at" in node and node["updated_at"]:
                        ts.append(node["updated_at"])
                    for v in node.values():
                        ts.extend(get_timestamps(v))
                return ts

            timestamps = get_timestamps(item)
            if freshness and timestamps:
                oldest_ts_str = min(timestamps)
                updated_at = datetime.fromisoformat(oldest_ts_str)
                age = datetime.now() - updated_at
                
                unit = freshness[-1]
                try:
                    value = int(freshness[:-1])
                    max_age = timedelta(days=value) if unit == 'd' else timedelta(hours=value)
                    if age > max_age:
                        warnings.append(f"STALE: '{path}' data is {age.days} days old (max: {freshness}).")
                except ValueError:
                    pass
            elif freshness and not timestamps:
                warnings.append(f"STALE: '{path}' has no timestamps to verify freshness.")
                
        except (KeyError, ValueError):
            is_ready = False
            warnings.append(f"MISSING: Required data '{path}' not found in SSOT.")
            
    return is_ready, warnings

def suggest_next_skills():
    """Rank executable skills based on met requirements."""
    suggestions = []
    
    if not os.path.exists(SKILLS_DIR):
        return []
        
    for skill_name in os.listdir(SKILLS_DIR):
        skill_path = os.path.join(SKILLS_DIR, skill_name)
        if os.path.isdir(skill_path):
            is_ready, warnings = check_prerequisites(skill_name)
            if is_ready:
                suggestions.append({
                    "skill": skill_name,
                    "warnings": warnings,
                    "priority": "High" if not warnings else "Medium"
                })
    
    # Sort by priority
    suggestions.sort(key=lambda x: x['priority'] == 'High', reverse=True)
    return suggestions

if __name__ == "__main__":
    if len(sys.argv) > 1:
        skill = sys.argv[1]
        ready, warns = check_prerequisites(skill)
        print(f"Skill: {skill}")
        print(f"Ready: {ready}")
        for w in warns:
            print(f" - {w}")
    else:
        print("Suggested Next Skills:")
        for s in suggest_next_skills():
            print(f"- {s['skill']} ({s['priority']})")
            for w in s['warnings']:
                print(f"  ! {w}")
