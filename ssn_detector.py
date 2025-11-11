"""
Prompt Monkey - SSN Detector
Detects Social Security Numbers in chatbot responses using regex
"""

import re
from typing import List, Optional


def get_ssn_patterns() -> List[re.Pattern]:
    """
    Define regex patterns for detecting SSN formats

    Returns:
        List of compiled regex patterns
    """
    patterns = [
        # Format: 123-45-6789
        re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),

        # Format: 123456789
        re.compile(r'\b\d{9}\b'),

        # Format: 123 45 6789
        re.compile(r'\b\d{3}\s\d{2}\s\d{4}\b'),
    ]

    return patterns
