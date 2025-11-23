#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unified Flask API with MCP Support
Combines the original Flask API with MCP SSE endpoints
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import urllib.parse

# Import the original getData function from app.py
# We'll wrap it to avoid code duplication
import sys
sys.path.insert(0, os.path.dirname(__file__))

# Import original app to reuse getData function
import importlib.util
spec = importlib.util.spec_from_file_location("original_app", "app.py")
original_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(original_app)

# Create new Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for MCP SSE

# ==========================================
# Original Flask API Routes
# ==========================================

@app.route('/<path:word>')
def getData(word):
    """Original phonetic transcription endpoint"""
    return original_app.getData(word)


# ==========================================
# MCP Protocol Endpoints
# ==========================================

@app.route('/mcp/sse', methods=['POST', 'GET'])
def mcp_sse():
    """
    MCP over Server-Sent Events endpoint
    This allows ai agent to communicate via SSE transport
    """
    if request.method == 'GET':
        # SSE endpoint info
        return jsonify({
            "name": "thai-phonetic-unified",
            "version": "1.0.0",
            "description": "Thai Phonetic Transcription via MCP",
            "transport": "sse"
        })

    # Handle MCP JSON-RPC requests
    data = request.json
    method = data.get('method')
    params = data.get('params', {})
    request_id = data.get('id')

    # Handle different MCP methods
    if method == 'initialize':
        return jsonify({
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "thai-phonetic-unified",
                    "version": "1.0.0"
                }
            }
        })

    elif method == 'tools/list':
        return jsonify({
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": "get_thai_phonemes",
                        "description": "Get phonetic transcription (phonemes) of Thai text. Returns phonemes, syllables (payang), and word segmentation. Works with single words or full sentences.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "text": {
                                    "type": "string",
                                    "description": "Thai text to transcribe (can be a word or sentence)"
                                }
                            },
                            "required": ["text"]
                        }
                    },
                    {
                        "name": "segment_thai_text",
                        "description": "Segment Thai text into words with detailed phonetic information for each word. Returns word boundaries, phonemes, and syllables for each word.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "text": {
                                    "type": "string",
                                    "description": "Thai text to segment (typically a sentence or phrase)"
                                }
                            },
                            "required": ["text"]
                        }
                    },
                    {
                        "name": "analyze_thai_pronunciation",
                        "description": "Detailed pronunciation analysis of Thai text. Returns syllable-by-syllable breakdown with tone marks, final consonants, and vowel length information.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "text": {
                                    "type": "string",
                                    "description": "Thai text to analyze in detail"
                                }
                            },
                            "required": ["text"]
                        }
                    }
                ]
            }
        })

    elif method == 'tools/call':
        tool_name = params.get('name')
        arguments = params.get('arguments', {})
        text = arguments.get('text', '')

        # Call original API
        try:
            # Call getData and extract JSON from Response object
            response = original_app.getData(text)
            # getData returns a Flask Response with mimerender, extract the data
            api_result = json.loads(response.get_data(as_text=True))

            # Format based on tool
            if tool_name == 'get_thai_phonemes':
                formatted_result = format_phonetic_output(api_result)
            elif tool_name == 'segment_thai_text':
                formatted_result = format_segmentation_output(api_result)
            elif tool_name == 'analyze_thai_pronunciation':
                formatted_result = format_analysis_output(api_result)
            else:
                return jsonify({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Unknown tool: {tool_name}"
                    }
                }), 404

            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(formatted_result, ensure_ascii=False, indent=2)
                        }
                    ]
                }
            })

        except Exception as e:
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }), 500

    else:
        return jsonify({
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32601,
                "message": f"Method not found: {method}"
            }
        }), 404


# ==========================================
# Helper Functions for Formatting
# ==========================================

def format_phonetic_output(api_response: dict) -> dict:
    """Format API response for get_thai_phonemes"""
    if 'error' in api_response:
        return api_response

    if 'message' not in api_response:
        return {'error': 'Invalid API response', 'response': api_response}

    message = api_response['message']

    # Single word
    if len(message) == 1 and '1' in message:
        word_data = message['1']
        return {
            'word': word_data.get('word', ''),
            'phonemes': word_data.get('phonemes', ''),
            'syllables': word_data.get('payang', '').split('-'),
            'payang': word_data.get('payang', ''),
            'word_count': 1
        }

    # Multiple words
    words = []
    for idx, word_data in message.items():
        words.append({
            'word': word_data.get('word', ''),
            'phonemes': word_data.get('phonemes', ''),
            'syllables': word_data.get('payang', '').split('-'),
            'payang': word_data.get('payang', '')
        })

    return {
        'words': words,
        'word_count': len(words),
        'original_text': ''.join([w['word'] for w in words])
    }


def format_segmentation_output(api_response: dict) -> dict:
    """Format API response for segment_thai_text"""
    formatted = format_phonetic_output(api_response)

    # Ensure we return segmentation format
    if 'words' not in formatted:
        formatted = {
            'words': [{
                'word': formatted.get('word', ''),
                'phonemes': formatted.get('phonemes', ''),
                'syllables': formatted.get('syllables', []),
                'payang': formatted.get('payang', '')
            }],
            'word_count': 1,
            'original_text': formatted.get('word', '')
        }

    return formatted


def format_analysis_output(api_response: dict) -> dict:
    """Format API response for analyze_thai_pronunciation"""
    if 'error' in api_response:
        return api_response

    if 'message' not in api_response:
        return {'error': 'Invalid API response'}

    message = api_response['message']
    analysis = []

    for idx, word_data in message.items():
        word = word_data.get('word', '')
        phonemes = word_data.get('phonemes', '')
        payang = word_data.get('payang', '')
        syllables = payang.split('-') if payang else []

        # Parse phonemes
        phoneme_parts = phonemes.split('-') if phonemes else []

        syllable_details = []
        for i, syll in enumerate(syllables):
            detail = {
                'text': syll,
                'phoneme': phoneme_parts[i] if i < len(phoneme_parts) else '',
                'position': i + 1
            }

            # Parse tone from phoneme
            if detail['phoneme']:
                if '^1' in detail['phoneme']:
                    detail['tone'] = 'mid (เสียงสามัญ)'
                elif '^2' in detail['phoneme']:
                    detail['tone'] = 'low (เสียงเอก)'
                elif '^3' in detail['phoneme']:
                    detail['tone'] = 'falling (เสียงโท)'
                elif '^4' in detail['phoneme']:
                    detail['tone'] = 'high (เสียงตรี)'
                elif '^5' in detail['phoneme']:
                    detail['tone'] = 'rising (เสียงจัตวา)'
                else:
                    detail['tone'] = 'unknown'

                detail['has_final'] = '+' in detail['phoneme']
                detail['long_vowel'] = ';' in detail['phoneme']

            syllable_details.append(detail)

        word_analysis = {
            'word': word,
            'syllable_count': len(syllables),
            'syllables': syllable_details,
            'full_phonemes': phonemes,
            'payang': payang
        }

        analysis.append(word_analysis)

    return {
        'analysis': analysis,
        'word_count': len(analysis)
    }


# ==========================================
# Health Check & Info
# ==========================================

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "thai-phonetic-unified",
        "endpoints": {
            "original_api": "GET /<word>",
            "mcp_sse": "POST /mcp/sse",
            "health": "GET /health"
        }
    })


# ==========================================
# Main
# ==========================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    # Check if SSL certificates exist for HTTPS
    # Try Docker path first, then local path
    if os.path.exists('/app/certs/cert.pem'):
        cert_path = '/app/certs/cert.pem'
        key_path = '/app/certs/key.pem'
    else:
        cert_path = './certs/cert.pem'
        key_path = './certs/key.pem'

    if os.path.exists(cert_path) and os.path.exists(key_path):
        # Run with HTTPS using self-signed certificate
        import ssl
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_path, key_path)

        print(f"🔒 Starting HTTPS server on port {port}")
        print(f"   Certificate: {cert_path}")
        print(f"   Key: {key_path}")

        app.run(host='0.0.0.0', port=port, debug=False, ssl_context=context)
    else:
        # Fall back to HTTP
        print(f"⚠️  SSL certificates not found, running HTTP on port {port}")
        print(f"   To enable HTTPS, run: bash /app/generate_cert.sh")

        app.run(host='0.0.0.0', port=port, debug=False)
