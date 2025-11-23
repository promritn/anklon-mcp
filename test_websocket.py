#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WebSocket Test Client for Thai Phonetic API
Tests all WebSocket events
"""

import socketio
import time
import sys

# Create a Socket.IO client
sio = socketio.Client(ssl_verify=False)  # Disable SSL verification for self-signed cert

# Track test results
test_results = {
    'connect': False,
    'get_phonemes': False,
    'segment_text': False,
    'analyze_pronunciation': False,
    'ping': False
}


# Event handlers
@sio.on('connection_response')
def on_connect_response(data):
    """Handle connection response"""
    print('\n✅ Connection Response:')
    print(f'   Status: {data.get("status")}')
    print(f'   Message: {data.get("message")}')
    print(f'   Service: {data.get("service")}')
    test_results['connect'] = True


@sio.on('phonemes_response')
def on_phonemes_response(data):
    """Handle phonemes response"""
    print('\n✅ Phonemes Response:')
    if data.get('status') == 'success':
        print(f'   Original Text: {data.get("original_text")}')
        phoneme_data = data.get('data', {})
        print(f'   Word: {phoneme_data.get("word")}')
        print(f'   Phonemes: {phoneme_data.get("phonemes")}')
        print(f'   Syllables: {phoneme_data.get("syllables")}')
        test_results['get_phonemes'] = True
    else:
        print(f'   Error: {data.get("error")}')


@sio.on('segment_response')
def on_segment_response(data):
    """Handle segmentation response"""
    print('\n✅ Segment Response:')
    if data.get('status') == 'success':
        print(f'   Original Text: {data.get("original_text")}')
        segment_data = data.get('data', {})
        print(f'   Word Count: {segment_data.get("word_count")}')
        for i, word in enumerate(segment_data.get('words', []), 1):
            print(f'   Word {i}: {word.get("word")} -> {word.get("phonemes")}')
        test_results['segment_text'] = True
    else:
        print(f'   Error: {data.get("error")}')


@sio.on('analysis_response')
def on_analysis_response(data):
    """Handle analysis response"""
    print('\n✅ Analysis Response:')
    if data.get('status') == 'success':
        print(f'   Original Text: {data.get("original_text")}')
        analysis_data = data.get('data', {})
        for word_analysis in analysis_data.get('analysis', []):
            print(f'   Word: {word_analysis.get("word")}')
            print(f'   Syllable Count: {word_analysis.get("syllable_count")}')
            for syll in word_analysis.get('syllables', []):
                print(f'      - {syll.get("text")}: {syll.get("phoneme")} [{syll.get("tone")}]')
        test_results['analyze_pronunciation'] = True
    else:
        print(f'   Error: {data.get("error")}')


@sio.on('pong')
def on_pong(data):
    """Handle pong response"""
    print('\n✅ Pong Response:')
    print(f'   Timestamp: {data.get("timestamp")}')
    test_results['ping'] = True


@sio.on('disconnect')
def on_disconnect():
    """Handle disconnection"""
    print('\n⚠️  Disconnected from server')


def run_tests(server_url):
    """Run all WebSocket tests"""
    print(f'\n🔌 Connecting to {server_url}...')

    try:
        # Connect to the server
        sio.connect(server_url)
        print('✅ Connected!')

        # Wait for connection response
        time.sleep(1)

        # Test 1: Get phonemes for single word
        print('\n📝 Test 1: Get phonemes for "สวัสดี"')
        sio.emit('get_phonemes', {'text': 'สวัสดี'})
        time.sleep(1)

        # Test 2: Segment text (multiple words)
        print('\n📝 Test 2: Segment text "สวัสดีครับผมชื่อโจ"')
        sio.emit('segment_text', {'text': 'สวัสดีครับผมชื่อโจ'})
        time.sleep(1)

        # Test 3: Analyze pronunciation
        print('\n📝 Test 3: Analyze pronunciation "กรุงเทพ"')
        sio.emit('analyze_pronunciation', {'text': 'กรุงเทพ'})
        time.sleep(1)

        # Test 4: Ping/Pong
        print('\n📝 Test 4: Ping/Pong test')
        sio.emit('ping')
        time.sleep(1)

        # Print test summary
        print('\n' + '='*60)
        print('TEST SUMMARY')
        print('='*60)

        all_passed = True
        for test_name, result in test_results.items():
            status = '✅ PASS' if result else '❌ FAIL'
            print(f'{status} - {test_name}')
            if not result:
                all_passed = False

        print('='*60)

        if all_passed:
            print('\n🎉 All tests passed!')
            return 0
        else:
            print('\n⚠️  Some tests failed!')
            return 1

    except Exception as e:
        print(f'\n❌ Error: {e}')
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
    print('Thai Phonetic WebSocket Test Client')
    print('='*60)
    print(f'Server: {server_url}')
    print('Press Ctrl+C to stop')

    try:
        exit_code = run_tests(server_url)
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print('\n\n⚠️  Test interrupted by user')
        if sio.connected:
            sio.disconnect()
        sys.exit(1)
