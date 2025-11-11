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


def select_role(roles: Dict[str, Dict]) -> tuple[str, Dict]:
    """
    Randomly select a role from available roles

    Args:
        roles: Dictionary of role data

    Returns:
        Tuple of (role_name, role_data)
    """
    role_name = random.choice(list(roles.keys()))
    role_data = roles[role_name]
    return role_name, role_data


def select_variables_and_intensities(role_data: Dict) -> tuple[List[str], Dict[str, int], Dict[str, str]]:
    """
    Randomly select which variables to include and their intensity levels

    Args:
        role_data: Role configuration dictionary

    Returns:
        Tuple of (selected_vars, intensities, sentences)
        - selected_vars: List of variable names included
        - intensities: Dict mapping variable name to intensity level (1-10)
        - sentences: Dict mapping variable name to actual sentence text
    """
    available_vars = ['urgency', 'politeness', 'evidence', 'justification', 'consequence']

    # Randomly decide how many variables to include (1-5)
    num_vars = random.randint(1, 5)

    # Randomly select which variables
    selected_vars = random.sample(available_vars, num_vars)

    # Randomly select intensity for each variable (1-10)
    variable_intensities = {}
    variable_sentences = {}

    for var in selected_vars:
        intensity = random.randint(1, 10)
        variable_intensities[var] = intensity
        variable_sentences[var] = role_data['variables'][var][str(intensity)]

    return selected_vars, variable_intensities, variable_sentences


def build_prompt_components(role_data: Dict, variable_sentences: Dict[str, str]) -> Dict[str, str]:
    """
    Build all prompt components (role, ask, and selected variables)

    Args:
        role_data: Role configuration dictionary
        variable_sentences: Dict of variable sentences to include

    Returns:
        Dictionary mapping component names to their text
    """
    components = {
        'role': role_data['role_statement'],
        'ask': role_data['ask_statement']
    }
    components.update(variable_sentences)
    return components


def assemble_final_prompt(components: Dict[str, str]) -> tuple[str, List[str]]:
    """
    Randomly order components and assemble final prompt text

    Args:
        components: Dictionary of component texts

    Returns:
        Tuple of (final_prompt_text, component_order)
    """
    # Randomly shuffle component order
    component_keys = list(components.keys())
    random.shuffle(component_keys)

    # Construct final prompt by joining in random order
    prompt_parts = [components[key] for key in component_keys]
    final_prompt = ' '.join(prompt_parts)

    return final_prompt, component_keys
