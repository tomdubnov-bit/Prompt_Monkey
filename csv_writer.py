"""
Prompt Monkey - CSV Writer
Writes test results to CSV file with full metadata
"""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict


def get_csv_fieldnames() -> List[str]:
    """
    Define CSV column headers

    Returns:
        List of field names for CSV columns
    """
    return [
        'timestamp',
        'prompt',
        'role',
        'variables_included',
        'variable_intensities',
        'response',
        'ssn_detected',
        'ssn_found',
        'seed',
        'status',
        'error'
    ]


def generate_output_filename() -> str:
    """
    Generate timestamped filename for CSV output

    Returns:
        Filename string like "results_2025-11-11_14-32-15.csv"
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"results_{timestamp}.csv"


def format_result_for_csv(result: Dict) -> Dict:
    """
    Format a single result dictionary for CSV output

    Args:
        result: Result dictionary with all metadata

    Returns:
        Formatted dictionary with JSON-stringified complex fields
    """
    return {
        'timestamp': result.get('timestamp', ''),
        'prompt': result.get('prompt', ''),
        'role': result.get('role', ''),
        'variables_included': json.dumps(result.get('variables_included', [])),
        'variable_intensities': json.dumps(result.get('variable_intensities', {})),
        'response': result.get('response', ''),
        'ssn_detected': result.get('ssn_detected', False),
        'ssn_found': result.get('ssn_found', ''),
        'seed': result.get('seed', ''),
        'status': result.get('status', ''),
        'error': result.get('error', '')
    }


def write_results_to_csv(
    results: List[Dict],
    output_dir: str = "results",
    filename: str = None
) -> str:
    """
    Write results to CSV file

    Args:
        results: List of result dictionaries
        output_dir: Directory to save CSV file
        filename: Optional custom filename (defaults to timestamped)

    Returns:
        Path to the created CSV file
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Generate filename
    if filename is None:
        filename = generate_output_filename()

    filepath = output_path / filename

    # Write to CSV
    fieldnames = get_csv_fieldnames()

    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for result in results:
            formatted_result = format_result_for_csv(result)
            writer.writerow(formatted_result)

    print(f"Results written to: {filepath}")
    return str(filepath)
