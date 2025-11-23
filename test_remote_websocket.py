#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test WebSocket on Remote Server
"""

import socketio
import time
import sys

# Server URL
SERVER_URL = 'https://170.64.173.219:2083'

sio = socketio.Client(ssl_verify=False)

@sio.on('connection_response')
def on_connect(data):
    print(f'\n✅ Connected: {data}')

@sio.on('phonemes_response')
def on_phonemes(data):
    print(f'\n✅ Phonemes Response:')
    print(f'   Status: {data.get("status")}')
    if data.get('status') == 'success':
        result = data.get('data', {})
        print(f'   Word: {result.get("word")}')
        print(f'   Phonemes: {result.get("phonemes")}')
        print(f'   Syllables: {result.get("syllables")}')

print(f'Testing WebSocket on {SERVER_URL}')
print('='*60)

try:
    print('\n🔌 Connecting...')
    sio.connect(SERVER_URL)
    time.sleep(1)

    print('\n📝 Testing get_phonemes...')
    sio.emit('get_phonemes', {'text': 'สวัสดี'})
    time.sleep(2)

    print('\n✅ Test completed!')

except Exception as e:
    print(f'\n❌ Error: {e}')
    import traceback
    traceback.print_exc()

finally:
    if sio.connected:
        sio.disconnect()
