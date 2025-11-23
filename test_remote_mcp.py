#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test MCP Protocol on Remote Server via WebSocket
"""

import socketio
import time
import json

# Server URL
SERVER_URL = 'https://170.64.173.219:2083'

sio = socketio.Client(ssl_verify=False)
request_id = 0

def get_id():
    global request_id
    request_id += 1
    return request_id

@sio.on('connection_response')
def on_connect(data):
    print(f'\n✅ Connected: {data.get("message")}')

@sio.on('mcp_response')
def on_mcp_response(data):
    req_id = data.get('id')

    if 'error' in data:
        print(f'\n❌ Error (ID {req_id}): {data["error"]}')
        return

    result = data.get('result', {})

    if req_id == 1:  # Initialize
        print(f'\n✅ Initialize:')
        print(f'   Protocol: {result.get("protocolVersion")}')
        print(f'   Server: {result.get("serverInfo", {}).get("name")}')

    elif req_id == 2:  # Tools list
        tools = result.get('tools', [])
        print(f'\n✅ Tools List ({len(tools)} tools):')
        for tool in tools:
            print(f'   - {tool.get("name")}')

    elif req_id == 3:  # Tools call
        print(f'\n✅ Tools Call Response:')
        content = result.get('content', [])
        if content:
            data_str = content[0].get('text', '')
            data_obj = json.loads(data_str)
            print(f'   Word: {data_obj.get("word")}')
            print(f'   Phonemes: {data_obj.get("phonemes")}')

print(f'Testing MCP Protocol on {SERVER_URL}')
print('='*60)

try:
    print('\n🔌 Connecting...')
    sio.connect(SERVER_URL)
    time.sleep(1)

    print('\n📝 Test 1: Initialize')
    sio.emit('mcp_request', {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {},
        "id": get_id()
    })
    time.sleep(1)

    print('\n📝 Test 2: Tools List')
    sio.emit('mcp_request', {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "params": {},
        "id": get_id()
    })
    time.sleep(1)

    print('\n📝 Test 3: Tools Call - get_thai_phonemes')
    sio.emit('mcp_request', {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "get_thai_phonemes",
            "arguments": {"text": "สวัสดี"}
        },
        "id": get_id()
    })
    time.sleep(2)

    print('\n✅ All tests completed!')

except Exception as e:
    print(f'\n❌ Error: {e}')
    import traceback
    traceback.print_exc()

finally:
    if sio.connected:
        sio.disconnect()
