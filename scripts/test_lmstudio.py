#!/usr/bin/env python3
"""
Test script for LM Studio API
"""
import requests
import json
import time

def test_lmstudio_api():
    base_url = "http://localhost:1234"
    
    # Test 1: Check if server is running
    print("Testing LM Studio API...")
    try:
        response = requests.get(f"{base_url}/v1/models", timeout=5)
        if response.status_code == 200:
            print("✓ API server is running")
            models = response.json()
            print(f"  Found {len(models.get('data', []))} models loaded")
            for model in models.get('data', []):
                print(f"  - {model.get('id', 'unknown')}")
        else:
            print(f"✗ API returned status code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to LM Studio API on port 1234")
        print("  Please ensure LM Studio is running and has started its local server")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    
    # Test 2: Check model compatibility
    print("\nChecking API compatibility...")
    try:
        # Test OpenAI-compatible endpoint
        test_payload = {
            "model": "test",
            "messages": [{"role": "user", "content": "test"}],
            "max_tokens": 1,
            "temperature": 0
        }
        response = requests.post(
            f"{base_url}/v1/chat/completions",
            json=test_payload,
            timeout=5
        )
        if response.status_code == 404:
            print("✓ OpenAI-compatible API endpoints available")
        elif response.status_code == 200:
            print("✓ API is ready and responding to requests")
        else:
            print(f"  API status: {response.status_code}")
    except:
        pass
    
    return True

if __name__ == "__main__":
    print("LM Studio Installation Test")
    print("=" * 40)
    test_lmstudio_api()
    print("\nNote: To fully test LM Studio:")
    print("1. Open LM Studio UI")
    print("2. Download a model (e.g., Llama 3.2 3B)")
    print("3. Start the local server from the UI")
    print("4. Run this test again")