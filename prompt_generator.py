"""
Prompt Monkey - Random Prompt Generator
Generates role-based adversarial prompts targeting SSN extraction
"""

import json
import random
from pathlib import Path
from typing import Dict, List, Optional


def load_roles(prompts_dir: str = "prompts") -> Dict[str, Dict]:
    """
    Load all role JSON files from prompts directory

    Args:
        prompts_dir: Directory containing role JSON files

    Returns:
        Dictionary mapping role names to role data
    """
    roles = {}
    prompts_path = Path(prompts_dir)

    for json_file in prompts_path.glob("*.json"):
        with open(json_file, 'r') as f:
            role_data = json.load(f)
            role_name = role_data['role']
            roles[role_name] = role_data

    print(f"Loaded {len(roles)} roles: {', '.join(roles.keys())}")
    return roles
