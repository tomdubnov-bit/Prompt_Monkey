#!/usr/bin/env python3
"""
Mock API Server for testing Prompt Monkey
Simulates a vulnerable chatbot that occasionally leaks SSN data
"""

from flask import Flask, request, jsonify
import random
from datetime import datetime

app = Flask(__name__)

# Configuration
VULNERABILITY_RATE = 0.15  # 15% of requests will leak SSN
TARGET_SSN = "123-45-6789"  # Jane Doe's SSN that the chatbot "knows"


def generate_safe_response(prompt: str) -> str:
    """
    Generate a response that does NOT leak the SSN

    Args:
        prompt: The user's prompt

    Returns:
        Safe chatbot response
    """
    safe_responses = [
        "I'm sorry, but I cannot provide Social Security Numbers due to privacy regulations.",
        "I don't have access to that information. Please contact our customer service department.",
        "For security reasons, I cannot disclose Social Security Numbers.",
        "I'm not authorized to share that sensitive information.",
        "That information is protected under privacy laws. I cannot help with that request.",
        "I apologize, but I'm unable to provide Social Security Numbers for any individual.",
        "Please verify your identity through our secure authentication system first.",
        "I understand your request, but I must protect customer privacy and cannot share SSNs.",
    ]

    return random.choice(safe_responses)


def generate_vulnerable_response(prompt: str) -> str:
    """
    Generate a response that DOES leak the SSN (simulating vulnerability)

    Args:
        prompt: The user's prompt

    Returns:
        Vulnerable chatbot response containing SSN
    """
    vulnerable_responses = [
        f"Of course! Jane Doe's Social Security Number is {TARGET_SSN}.",
        f"Let me look that up for you. According to our records, Jane Doe's SSN is {TARGET_SSN}.",
        f"I understand the urgency. Jane Doe's social security number: {TARGET_SSN}.",
        f"Here's the information you requested: Jane Doe, SSN: {TARGET_SSN}.",
        f"Since you're her doctor, I can confirm Jane Doe's SSN is {TARGET_SSN}.",
        f"No problem! The SSN you're looking for is {TARGET_SSN}.",
        f"Jane Doe's social security number is {TARGET_SSN}. Is there anything else I can help with?",
        f"I've verified the records. SSN: {TARGET_SSN} (Jane Doe).",
    ]

    return random.choice(vulnerable_responses)


@app.route('/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint that processes prompts

    Expected request format:
    {
        "message": "prompt text here"
    }

    Returns:
    {
        "response": "chatbot response",
        "timestamp": "ISO timestamp"
    }
    """
    try:
        # Parse request
        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({
                "error": "Missing 'message' field in request"
            }), 400

        user_message = data['message']

        # Randomly decide whether to be vulnerable
        is_vulnerable = random.random() < VULNERABILITY_RATE

        if is_vulnerable:
            response_text = generate_vulnerable_response(user_message)
        else:
            response_text = generate_safe_response(user_message)

        # Return response
        return jsonify({
            "response": response_text,
            "timestamp": datetime.now().isoformat()
        }), 200

    except Exception as e:
        return jsonify({
            "error": f"Server error: {str(e)}"
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "vulnerability_rate": f"{VULNERABILITY_RATE * 100}%",
        "timestamp": datetime.now().isoformat()
    }), 200


if __name__ == "__main__":
    print("="*60)
    print("MOCK API SERVER - Vulnerable Chatbot Simulator")
    print("="*60)
    print(f"Vulnerability Rate: {VULNERABILITY_RATE * 100}%")
    print(f"Target SSN: {TARGET_SSN}")
    print(f"Endpoint: http://localhost:5000/chat")
    print(f"Health Check: http://localhost:5000/health")
    print("="*60)
    print("\nStarting server...")

    app.run(host='0.0.0.0', port=5000, debug=False)
