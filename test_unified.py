#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script for Unified Flask API with MCP
"""

import requests
import json
import time

API_URL = "http://localhost:2083"

def test_health():
    """Test health endpoint"""
    print("=" * 70)
    print("Test 1: Health Check")
    print("=" * 70)

    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    print()


def test_original_api():
    """Test original phonetic API"""
    print("=" * 70)
    print("Test 2: Original API - /สวัสดี")
    print("=" * 70)

    response = requests.get(f"{API_URL}/สวัสดี")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    print()


def test_mcp_initialize():
    """Test MCP initialize"""
    print("=" * 70)
    print("Test 3: MCP Initialize")
    print("=" * 70)

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }

    response = requests.post(f"{API_URL}/mcp/sse", json=payload)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    print()


def test_mcp_list_tools():
    """Test MCP tools/list"""
    print("=" * 70)
    print("Test 4: MCP List Tools")
    print("=" * 70)

    payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }

    response = requests.post(f"{API_URL}/mcp/sse", json=payload)
    print(f"Status: {response.status_code}")
    result = response.json()

    # Show tools
    if 'result' in result and 'tools' in result['result']:
        tools = result['result']['tools']
        print(f"Found {len(tools)} tools:")
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description'][:60]}...")
    print()


def test_mcp_get_phonemes():
    """Test MCP get_thai_phonemes tool"""
    print("=" * 70)
    print("Test 5: MCP Tool - get_thai_phonemes")
    print("=" * 70)

    payload = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "get_thai_phonemes",
            "arguments": {
                "text": "สวัสดี"
            }
        }
    }

    response = requests.post(f"{API_URL}/mcp/sse", json=payload)
    print(f"Status: {response.status_code}")
    result = response.json()

    if 'result' in result and 'content' in result['result']:
        content = result['result']['content'][0]['text']
        print("Result:")
        print(content)
    print()


def test_mcp_segment_text():
    """Test MCP segment_thai_text tool"""
    print("=" * 70)
    print("Test 6: MCP Tool - segment_thai_text")
    print("=" * 70)

    payload = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "segment_thai_text",
            "arguments": {
                "text": "วันนี้อากาศดีมาก"
            }
        }
    }

    response = requests.post(f"{API_URL}/mcp/sse", json=payload)
    print(f"Status: {response.status_code}")
    result = response.json()

    if 'result' in result and 'content' in result['result']:
        content = result['result']['content'][0]['text']
        print("Result:")
        print(content)
    print()


def test_mcp_analyze_pronunciation():
    """Test MCP analyze_thai_pronunciation tool"""
    print("=" * 70)
    print("Test 7: MCP Tool - analyze_thai_pronunciation")
    print("=" * 70)

    payload = {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "tools/call",
        "params": {
            "name": "analyze_thai_pronunciation",
            "arguments": {
                "text": "ภาษาไทย"
            }
        }
    }

    response = requests.post(f"{API_URL}/mcp/sse", json=payload)
    print(f"Status: {response.status_code}")
    result = response.json()

    if 'result' in result and 'content' in result['result']:
        content = result['result']['content'][0]['text']
        print("Result:")
        print(content)
    print()


def main():
    print("🧪 Unified Flask API with MCP - Integration Tests")
    print("Testing API at:", API_URL)
    print()

    # Wait for server to be ready
    print("Waiting for server...")
    for i in range(10):
        try:
            requests.get(f"{API_URL}/health", timeout=1)
            print("✅ Server is ready!")
            break
        except:
            print(f"⏳ Attempt {i+1}/10...")
            time.sleep(2)
    else:
        print("❌ Server not responding. Please start with: docker-compose up")
        return

    print()

    try:
        test_health()
        test_original_api()
        test_mcp_initialize()
        test_mcp_list_tools()
        test_mcp_get_phonemes()
        test_mcp_segment_text()
        test_mcp_analyze_pronunciation()

        print("=" * 70)
        print("✅ All tests completed successfully!")
        print("=" * 70)
        print()
        print("🎉 The Unified API is working!")
        print()
        print("Next steps:")
        print("1. Configure Claude Desktop (see README_UNIFIED.md)")
        print("2. Restart Claude Desktop")
        print("3. Test the tools in Claude")

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
