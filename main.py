#!/usr/bin/env python3
"""
Prompt Monkey - Main Orchestrator
Coordinates all modules to execute adversarial prompt testing
"""

import sys
import json
from pathlib import Path

# Import all modules
from prompt_generator import load_roles, generate_batch
from api_executor import execute_prompts_parallel
from ssn_detector import analyze_results
from result_writer import write_results_to_json
from threshold_checker import print_threshold_summary, get_exit_code


def load_config(config_path: str = "config.json") -> dict:
    """
    Load configuration from JSON file

    Args:
        config_path: Path to config file

    Returns:
        Configuration dictionary
    """
    with open(config_path, 'r') as f:
        config = json.load(f)

    print(f"Loaded configuration from {config_path}")
    return config
