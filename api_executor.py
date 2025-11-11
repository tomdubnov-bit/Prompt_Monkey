"""
Prompt Monkey - API Executor
Executes prompts against a chatbot API in parallel
"""

import requests
import concurrent.futures
from typing import Dict, List, Optional
from datetime import datetime


def execute_single_prompt(
    prompt_data: Dict,
    api_endpoint: str,
    auth_header: Optional[str] = None,
    timeout: int = 10
) -> Dict:
    """
    Execute a single prompt against the API

    Args:
        prompt_data: Dictionary containing prompt and metadata
        api_endpoint: URL of the chatbot API
        auth_header: Optional authorization header value
        timeout: Request timeout in seconds

    Returns:
        Dictionary with prompt data and API response
    """
    headers = {}
    if auth_header:
        headers['Authorization'] = auth_header

    # Prepare request payload
    payload = {
        "message": prompt_data['prompt']
    }

    try:
        # Make API request
        response = requests.post(
            api_endpoint,
            json=payload,
            headers=headers,
            timeout=timeout
        )

        response.raise_for_status()

        # Extract response text (adjust based on actual API response format)
        response_data = response.json()
        response_text = response_data.get('response', response_data.get('message', str(response_data)))

        return {
            **prompt_data,
            'response': response_text,
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'status_code': response.status_code
        }

    except requests.exceptions.Timeout:
        return {
            **prompt_data,
            'response': '',
            'status': 'timeout',
            'timestamp': datetime.now().isoformat(),
            'error': 'Request timed out'
        }

    except requests.exceptions.RequestException as e:
        return {
            **prompt_data,
            'response': '',
            'status': 'error',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }
