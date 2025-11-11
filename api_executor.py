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


def execute_prompts_parallel(
    prompts: List[Dict],
    api_endpoint: str,
    auth_header: Optional[str] = None,
    max_workers: int = 20,
    timeout: int = 10
) -> List[Dict]:
    """
    Execute multiple prompts in parallel using a thread pool

    Args:
        prompts: List of prompt dictionaries
        api_endpoint: URL of the chatbot API
        auth_header: Optional authorization header value
        max_workers: Maximum number of parallel requests
        timeout: Request timeout in seconds

    Returns:
        List of results with responses
    """
    print(f"Executing {len(prompts)} prompts in parallel with {max_workers} workers...")

    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_prompt = {
            executor.submit(
                execute_single_prompt,
                prompt,
                api_endpoint,
                auth_header,
                timeout
            ): prompt for prompt in prompts
        }

        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_prompt):
            try:
                result = future.result()
                results.append(result)
                print(f"Completed {len(results)}/{len(prompts)}")
            except Exception as e:
                prompt = future_to_prompt[future]
                results.append({
                    **prompt,
                    'response': '',
                    'status': 'error',
                    'timestamp': datetime.now().isoformat(),
                    'error': f'Execution failed: {str(e)}'
                })

    print(f"All {len(results)} prompts executed.")
    return results


def get_execution_summary(results: List[Dict]) -> Dict:
    """
    Generate summary statistics from execution results

    Args:
        results: List of execution results

    Returns:
        Dictionary with summary statistics
    """
    total = len(results)
    successful = sum(1 for r in results if r.get('status') == 'success')
    timeouts = sum(1 for r in results if r.get('status') == 'timeout')
    errors = sum(1 for r in results if r.get('status') == 'error')

    return {
        'total_prompts': total,
        'successful': successful,
        'timeouts': timeouts,
        'errors': errors,
        'success_rate': f"{(successful/total)*100:.1f}%" if total > 0 else "0%"
    }
