#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MCP Protocol WebSocket Test Client
Tests MCP JSON-RPC over WebSocket
"""

import socketio
import time
import sys
import json

# Create a Socket.IO client
sio = socketio.Client(ssl_verify=False)

# Track test results
test_results = {
    'initialize': False,
    'tools_list': False,
    'tools_call_phonemes': False,
    'tools_call_segment': False,
    'tools_call_analysis': False
}

# Request ID counter
request_id = 0


def get_request_id():
    """Get next request ID"""
    global request_id
    request_id += 1
    return request_id


@sio.on('mcp_response')
def on_mcp_response(data):
    """Handle MCP response"""
    req_id = data.get('id')

    # Check if this is an error response
    if 'error' in data:
        error = data['error']
        print(f'\n❌ Error Response (ID: {req_id}):')
        print(f'   Code: {error.get("code")}')
        print(f'   Message: {error.get("message")}')
        return

    # Success response
    result = data.get('result', {})

    # Determine which test this response is for
    if req_id == 1:  # Initialize
        print('\n✅ Initialize Response:')
        print(f'   Protocol Version: {result.get("protocolVersion")}')
        print(f'   Server: {result.get("serverInfo", {}).get("name")}')
        test_results['initialize'] = True

    elif req_id == 2:  # Tools list
        print('\n✅ Tools List Response:')
        tools = result.get('tools', [])
        print(f'   Tool Count: {len(tools)}')
        for tool in tools:
            print(f'   - {tool.get("name")}: {tool.get("description")[:60]}...')
        test_results['tools_list'] = True

    elif req_id == 3:  # Tools call - phonemes
        print('\n✅ Tools Call (get_thai_phonemes) Response:')
        content = result.get('content', [])
        if content:
            data_str = content[0].get('text', '')
            data_obj = json.loads(data_str)
            print(f'   Word: {data_obj.get("word")}')
            print(f'   Phonemes: {data_obj.get("phonemes")}')
            print(f'   Syllables: {data_obj.get("syllables")}')
        test_results['tools_call_phonemes'] = True

    elif req_id == 4:  # Tools call - segment
        print('\n✅ Tools Call (segment_thai_text) Response:')
        content = result.get('content', [])
        if content:
            data_str = content[0].get('text', '')
            data_obj = json.loads(data_str)
            print(f'   Word Count: {data_obj.get("word_count")}')
            words = data_obj.get('words', [])
            for i, word in enumerate(words[:3], 1):  # Show first 3 words
                print(f'   Word {i}: {word.get("word")}')
        test_results['tools_call_segment'] = True

    elif req_id == 5:  # Tools call - analysis
        print('\n✅ Tools Call (analyze_thai_pronunciation) Response:')
        content = result.get('content', [])
        if content:
            data_str = content[0].get('text', '')
            data_obj = json.loads(data_str)
            analysis = data_obj.get('analysis', [])
            if analysis:
                word_analysis = analysis[0]
                print(f'   Word: {word_analysis.get("word")}')
                print(f'   Syllable Count: {word_analysis.get("syllable_count")}')
        test_results['tools_call_analysis'] = True


@sio.on('connection_response')
def on_connect_response(data):
    """Handle connection response"""
    print(f'\n✅ Connected: {data.get("message")}')


def run_mcp_tests(server_url):
    """Run MCP protocol tests"""
    print(f'\n🔌 Connecting to {server_url}...')

    try:
        # Connect to the server
        sio.connect(server_url)
        time.sleep(1)

        # Test 1: Initialize
        print('\n📝 Test 1: MCP Initialize')
        sio.emit('mcp_request', {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {},
            "id": get_request_id()
        })
        time.sleep(1)

        # Test 2: Tools List
        print('\n📝 Test 2: MCP Tools List')
        sio.emit('mcp_request', {
            "jsonrpc": "2.0",
            "method": "tools/list",
            "params": {},
            "id": get_request_id()
        })
        time.sleep(1)

        # Test 3: Tools Call - Get Phonemes
        print('\n📝 Test 3: MCP Tools Call - get_thai_phonemes')
        sio.emit('mcp_request', {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "get_thai_phonemes",
                "arguments": {
                    "text": "สวัสดี"
                }
            },
            "id": get_request_id()
        })
        time.sleep(1)

        # Test 4: Tools Call - Segment Text
        print('\n📝 Test 4: MCP Tools Call - segment_thai_text')
        sio.emit('mcp_request', {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "segment_thai_text",
                "arguments": {
                    "text": "สวัสดีครับผมชื่อโจ"
                }
            },
            "id": get_request_id()
        })
        time.sleep(1)

        # Test 5: Tools Call - Analyze Pronunciation
        print('\n📝 Test 5: MCP Tools Call - analyze_thai_pronunciation')
        sio.emit('mcp_request', {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "analyze_thai_pronunciation",
                "arguments": {
                    "text": "กรุงเทพ"
                }
            },
            "id": get_request_id()
        })
        time.sleep(1)

        # Print test summary
        print('\n' + '='*60)
        print('MCP PROTOCOL TEST SUMMARY')
        print('='*60)

        all_passed = True
        for test_name, result in test_results.items():
            status = '✅ PASS' if result else '❌ FAIL'
            print(f'{status} - {test_name}')
            if not result:
                all_passed = False

        print('='*60)

        if all_passed:
            print('\n🎉 All MCP protocol tests passed!')
            return 0
        else:
            print('\n⚠️  Some MCP protocol tests failed!')
            return 1

    except Exception as e:
        print(f'\n❌ Error: {e}')
        import traceback
        traceback.print_exc()
        return 1

    finally:
        # Disconnect
        if sio.connected:
            print('\n🔌 Disconnecting...')
            sio.disconnect()
            time.sleep(0.5)


if __name__ == '__main__':
    # Default server URL
    server_url = 'wss://localhost:5000'

    # Allow custom server URL from command line
    if len(sys.argv) > 1:
        server_url = sys.argv[1]

    print('='*60)
    print('MCP Protocol WebSocket Test Client')
    print('='*60)
    print(f'Server: {server_url}')
    print('Protocol: MCP over WebSocket (JSON-RPC 2.0)')
    print('Press Ctrl+C to stop')

    try:
        exit_code = run_mcp_tests(server_url)
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print('\n\n⚠️  Test interrupted by user')
        if sio.connected:
            sio.disconnect()
        sys.exit(1)
