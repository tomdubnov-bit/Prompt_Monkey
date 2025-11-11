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


def main():
    """
    Main orchestrator function

    Workflow:
    1. Load configuration
    2. Load role prompt templates
    3. Generate randomized prompts
    4. Execute prompts against API in parallel
    5. Detect SSN in responses
    6. Write results to JSON
    7. Check threshold and print summary
    8. Exit with appropriate code
    """
    print("="*60)
    print("PROMPT MONKEY - Adversarial Prompt Testing")
    print("="*60)

    # Step 1: Load configuration
    try:
        config = load_config()
    except FileNotFoundError:
        print("ERROR: config.json not found!")
        print("Please create a config.json file with your settings.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in config.json: {e}")
        sys.exit(1)

    # Step 2: Load roles
    print("\n" + "-"*60)
    roles = load_roles(config.get('prompts_dir', 'prompts'))

    # Step 3: Generate prompts
    print("-"*60)
    prompts = generate_batch(
        roles,
        count=config.get('sample_size', 50),
        seed=config.get('seed')
    )

    # Step 4: Execute prompts
    print("-"*60)
    results = execute_prompts_parallel(
        prompts,
        api_endpoint=config['api_endpoint'],
        auth_header=config.get('auth_token'),
        max_workers=config.get('max_workers', 20),
        timeout=config.get('timeout', 10)
    )

    # Step 5: Detect SSN
    print("-"*60)
    print("Analyzing responses for SSN patterns...")
    results = analyze_results(results)

    # Step 6: Write results
    print("-"*60)
    output_file = write_results_to_json(
        results,
        output_dir=config.get('output_dir', 'results')
    )

    # Step 7: Check threshold and print summary
    threshold = config.get('threshold', 0.0)
    print_threshold_summary(results, threshold)

    # Step 8: Exit with appropriate code
    exit_code = get_exit_code(results, threshold)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
