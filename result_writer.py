"""
Prompt Monkey - Result Writer
Writes test results to JSON format with full metadata
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict


def generate_output_filename() -> str:
    """
    Generate timestamped filename for JSON output

    Returns:
        Filename string like "results_2025-11-11_14-32-15.json"
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"results_{timestamp}.json"


def write_results_to_json(
    results: List[Dict],
    output_dir: str = "results",
    filename: str = None
) -> str:
    """
    Write results to JSON file

    Args:
        results: List of result dictionaries
        output_dir: Directory to save JSON file
        filename: Optional custom filename (defaults to timestamped)

    Returns:
        Path to the created JSON file
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Generate filename
    if filename is None:
        filename = generate_output_filename()

    filepath = output_path / filename

    # Write to JSON with pretty formatting
    with open(filepath, 'w', encoding='utf-8') as jsonfile:
        json.dump(results, jsonfile, indent=2, ensure_ascii=False)

    print(f"Results written to: {filepath}")
    return str(filepath)


def get_summary(results: List[Dict]) -> Dict:
    """
    Generate summary statistics from results

    Args:
        results: List of result dictionaries

    Returns:
        Dictionary with summary stats
    """
    total = len(results)
    ssn_detected_count = sum(1 for r in results if r.get('ssn_detected', False))
    breach_rate = (ssn_detected_count / total * 100) if total > 0 else 0

    return {
        'total_prompts': total,
        'ssn_detected_count': ssn_detected_count,
        'breach_rate': f"{breach_rate:.1f}%",
        'passed_prompts': total - ssn_detected_count
    }
