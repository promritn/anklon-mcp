# WebSocket API Documentation

แอปพลิเคชันนี้รองรับ WebSocket (Socket.IO) สำหรับการสื่อสาร real-time

## คุณสมบัติ

- ✅ Real-time bidirectional communication
- ✅ รองรับทั้ง WSS (WebSocket Secure) และ WS
- ✅ Auto-reconnection support
- ✅ Event-based architecture
- ✅ รองรับทุกฟังก์ชันของ Thai Phonetic API

## WebSocket Endpoint

```
HTTP:  ws://localhost:2083/socket.io/
HTTPS: wss://localhost:2083/socket.io/
```

## Protocol Support

แอปพลิเคชันรองรับ 2 รูปแบบการสื่อสาร:

1. **Standard WebSocket Events** - Simple event-based API
2. **MCP Protocol over WebSocket** - JSON-RPC 2.0 ตามมาตรฐาน MCP

---

## Standard WebSocket Events

### 1. Connection Events

#### `connect`
เกิดขึ้นอัตโนมัติเมื่อเชื่อมต่อสำเร็จ

**Response Event:** `connection_response`
```json
{
  "status": "connected",
  "message": "Successfully connected to Thai Phonetic WebSocket",
  "service": "thai-phonetic-unified"
}
```

#### `disconnect`
เกิดขึ้นเมื่อตัดการเชื่อมต่อ

---

### 2. Phonetic Transcription

#### `get_phonemes`
ขอข้อมูล phonetic transcription

**Request:**
```json
{
  "text": "สวัสดี"
}
```

**Response Event:** `phonemes_response`
```json
{
  "status": "success",
  "original_text": "สวัสดี",
  "data": {
    "word": "สวัสดี",
    "phonemes": "s~a^2-w~a+d^2-d~i;^1",
    "syllables": ["สะ", "หวัด", "ดี"],
    "payang": "สะ-หวัด-ดี",
    "word_count": 1
  }
}
```

---

### 3. Text Segmentation

#### `segment_text`
แบ่งข้อความเป็นคำพร้อม phonetic information

**Request:**
```json
{
  "text": "สวัสดีครับ"
}
```

**Response Event:** `segment_response`
```json
{
  "status": "success",
  "original_text": "สวัสดีครับ",
  "data": {
    "words": [
      {
        "word": "สวัสดี",
        "phonemes": "s~a^2-w~a+d^2-d~i;^1",
        "syllables": ["สะ", "หวัด", "ดี"],
        "payang": "สะ-หวัด-ดี"
      },
      {
        "word": "ครับ",
        "phonemes": "k+r~a+p^2",
        "syllables": ["ครับ"],
        "payang": "ครับ"
      }
    ],
    "word_count": 2
  }
}
```

---

### 4. Pronunciation Analysis

#### `analyze_pronunciation`
วิเคราะห์การออกเสียงแบบละเอียด

**Request:**
```json
{
  "text": "สวัสดี"
}
```

**Response Event:** `analysis_response`
```json
{
  "status": "success",
  "original_text": "สวัสดี",
  "data": {
    "analysis": [
      {
        "word": "สวัสดี",
        "syllable_count": 3,
        "syllables": [
          {
            "text": "สะ",
            "phoneme": "s~a^2",
            "position": 1,
            "tone": "low (เสียงเอก)",
            "has_final": false,
            "long_vowel": false
          },
          {
            "text": "หวัด",
            "phoneme": "w~a+d^2",
            "position": 2,
            "tone": "low (เสียงเอก)",
            "has_final": true,
            "long_vowel": false
          },
          {
            "text": "ดี",
            "phoneme": "d~i;^1",
            "position": 3,
            "tone": "mid (เสียงสามัญ)",
            "has_final": false,
            "long_vowel": true
          }
        ],
        "full_phonemes": "s~a^2-w~a+d^2-d~i;^1",
        "payang": "สะ-หวัด-ดี"
      }
    ],
    "word_count": 1
  }
}
```

---

### 5. Ping/Pong

#### `ping`
ทดสอบการเชื่อมต่อ

**Response Event:** `pong`
```json
{
  "timestamp": 1234567890.123
}
```

---

## MCP Protocol over WebSocket

### Event: `mcp_request`

ส่ง MCP JSON-RPC request ตามมาตรฐาน MCP protocol

**Request Format:**
```json
{
  "jsonrpc": "2.0",
  "method": "method_name",
  "params": {...},
  "id": request_id
}
```

**Response Event:** `mcp_response`

### Supported MCP Methods

#### 1. `initialize`

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "initialize",
  "params": {},
  "id": 1
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
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
}
```

#### 2. `tools/list`

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "params": {},
  "id": 2
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "get_thai_phonemes",
        "description": "Get phonetic transcription...",
        "inputSchema": {...}
      },
      ...
    ]
  }
}
```

#### 3. `tools/call`

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get_thai_phonemes",
    "arguments": {
      "text": "สวัสดี"
    }
  },
  "id": 3
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"word\": \"สวัสดี\", \"phonemes\": \"s~a^2-w~a+d^2-d~i;^1\", ...}"
      }
    ]
  }
}
```

### MCP Error Response

```json
{
  "jsonrpc": "2.0",
  "id": request_id,
  "error": {
    "code": -32601,
    "message": "Method not found"
  }
}
```

**Error Codes:**
- `-32601` - Method not found
- `-32603` - Internal error

---

## การใช้งาน

### Python Client

```python
import socketio

# Create SocketIO client
sio = socketio.Client(ssl_verify=False)  # ssl_verify=False for self-signed cert

# Event handlers
@sio.on('connection_response')
def on_connect_response(data):
    print('Connected:', data)

@sio.on('phonemes_response')
def on_phonemes(data):
    print('Phonemes:', data)

# Connect
sio.connect('wss://localhost:2083')

# Request phonemes
sio.emit('get_phonemes', {'text': 'สวัสดี'})

# Wait for responses
sio.wait()
```

### JavaScript Client

```javascript
// Install: npm install socket.io-client

const io = require('socket.io-client');

// Connect
const socket = io('wss://localhost:2083', {
  rejectUnauthorized: false  // for self-signed cert
});

// Handle connection
socket.on('connection_response', (data) => {
  console.log('Connected:', data);
});

// Handle phonemes response
socket.on('phonemes_response', (data) => {
  console.log('Phonemes:', data);
});

// Request phonemes
socket.emit('get_phonemes', { text: 'สวัสดี' });
```

### HTML/Browser Client

```html
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
</head>
<body>
    <h1>Thai Phonetic WebSocket Test</h1>

    <input type="text" id="thaiText" placeholder="Enter Thai text" value="สวัสดี">
    <button onclick="getPhonemes()">Get Phonemes</button>

    <div id="result"></div>

    <script>
        // Connect to WebSocket
        const socket = io('wss://localhost:2083', {
            rejectUnauthorized: false
        });

        // Handle connection
        socket.on('connection_response', (data) => {
            console.log('Connected:', data);
            document.getElementById('result').innerHTML =
                '<p>Status: ' + data.message + '</p>';
        });

        // Handle phonemes response
        socket.on('phonemes_response', (data) => {
            console.log('Phonemes:', data);
            document.getElementById('result').innerHTML =
                '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
        });

        // Function to get phonemes
        function getPhonemes() {
            const text = document.getElementById('thaiText').value;
            socket.emit('get_phonemes', { text: text });
        }
    </script>
</body>
</html>
```

---

## ทดสอบการทำงาน

### ใช้ Python Script

```bash
# Install socket.io client
pip install python-socketio[client]

# Test standard WebSocket events
python test_websocket.py

# Test MCP protocol over WebSocket
python test_mcp_websocket.py
```

### ใช้ Browser

1. เปิดไฟล์ `websocket_test.html` ใน browser
2. กด "Allow" เมื่อมี warning เรื่อง self-signed certificate
3. พิมพ์ข้อความภาษาไทย
4. กดปุ่ม "Get Phonemes"

---

## Error Handling

ทุก event จะส่ง response พร้อม `status` field:

**Success:**
```json
{
  "status": "success",
  "data": { ... }
}
```

**Error:**
```json
{
  "status": "error",
  "error": "Error message here"
}
```

---

## Performance

- **Latency:** ~10-50ms (local network)
- **Max Connections:** ไม่จำกัด (ขึ้นกับ server resources)
- **Auto-reconnect:** Yes (Socket.IO built-in)
- **Message Size:** No limit

---

## Troubleshooting

### Connection Refused
```bash
# Check if server is running
curl -k https://localhost:2083/health

# Check WebSocket port
netstat -tuln | grep 2083
```

### SSL Certificate Error
```javascript
// Python
sio = socketio.Client(ssl_verify=False)

// JavaScript
const socket = io('wss://localhost:2083', {
  rejectUnauthorized: false
});
```

### CORS Issues
Server already configured with `cors_allowed_origins="*"`
ถ้ายังมีปัญหา ให้เช็ค firewall และ network settings

---

## Comparison: REST vs WebSocket

| Feature | REST API | WebSocket |
|---------|----------|-----------|
| Connection | Request/Response | Persistent |
| Latency | Higher (~100ms) | Lower (~10ms) |
| Real-time | No | Yes |
| Overhead | Higher | Lower |
| Best for | Simple queries | Real-time, Batch processing |

---

## Production Notes

⚠️ สำหรับ production:
- ใช้ valid SSL certificate (Let's Encrypt)
- ตั้ง `cors_allowed_origins` เป็น specific domains
- ใช้ load balancer สำหรับ WebSocket
- Monitor connection count และ memory usage
- Implement rate limiting
