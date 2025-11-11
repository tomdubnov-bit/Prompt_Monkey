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
