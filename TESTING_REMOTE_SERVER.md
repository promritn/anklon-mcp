# คู่มือทดสอบ Remote Server

Server: **170.64.173.219:2083**

---

## 🔍 Quick Test (Health Check)

```bash
# ทดสอบว่า server ทำงานหรือไม่
curl -k https://170.64.173.219:2083/health
```

**ผลลัพธ์ที่ควรได้:**
```json
{
  "status": "healthy",
  "service": "thai-phonetic-unified",
  "endpoints": {...},
  "websocket_events": {...}
}
```

---

## 1️⃣ ทดสอบ REST API

### คำเดียว
```bash
curl -k https://170.64.173.219:2083/สวัสดี
```

### ประโยค
```bash
curl -k https://170.64.173.219:2083/สวัสดีครับผมชื่อโจ
```

### ผลลัพธ์ตัวอย่าง:
```json
{
  "message": {
    "1": {
      "word": "สวัสดี",
      "phonemes": "s~a^2-w~a+d^2-d~i;^1",
      "payang": "สะ-หวัด-ดี"
    }
  }
}
```

---

## 2️⃣ ทดสอบ MCP SSE Endpoint

### Initialize
```bash
curl -k -X POST https://170.64.173.219:2083/mcp/sse \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "initialize",
    "params": {},
    "id": 1
  }'
```

### Tools List
```bash
curl -k -X POST https://170.64.173.219:2083/mcp/sse \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "params": {},
    "id": 2
  }'
```

### Tools Call
```bash
curl -k -X POST https://170.64.173.219:2083/mcp/sse \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "get_thai_phonemes",
      "arguments": {
        "text": "สวัสดี"
      }
    },
    "id": 3
  }'
```

---

## 3️⃣ ทดสอบ WebSocket (Python)

### Standard WebSocket Events

```bash
# รัน script ทดสอบ
python test_remote_websocket.py
```

**ควรเห็นผลลัพธ์:**
```
Testing WebSocket on https://170.64.173.219:2083
============================================================

🔌 Connecting...

✅ Connected: {'status': 'connected', 'message': '...', ...}

📝 Testing get_phonemes...

✅ Phonemes Response:
   Status: success
   Word: สวัสดี
   Phonemes: s~a^2-w~a+d^2-d~i;^1
   Syllables: ['สะ', 'หวัด', 'ดี']

✅ Test completed!
```

### MCP Protocol WebSocket

```bash
# รัน script ทดสอบ MCP
python test_remote_mcp.py
```

**ควรเห็นผลลัพธ์:**
```
Testing MCP Protocol on https://170.64.173.219:2083
============================================================

🔌 Connecting...

✅ Connected: Successfully connected to Thai Phonetic WebSocket

📝 Test 1: Initialize

✅ Initialize:
   Protocol: 2024-11-05
   Server: thai-phonetic-unified

📝 Test 2: Tools List

✅ Tools List (3 tools):
   - get_thai_phonemes
   - segment_thai_text
   - analyze_thai_pronunciation

📝 Test 3: Tools Call - get_thai_phonemes

✅ Tools Call Response:
   Word: สวัสดี
   Phonemes: s~a^2-w~a+d^2-d~i;^1

✅ All tests completed!
```

---

## 4️⃣ ทดสอบผ่าน Browser

### วิธีที่ 1: เปิดไฟล์ HTML โดยตรง

1. เปิดไฟล์ `test_browser.html` ใน browser
2. คลิกปุ่ม **"Connect"**
3. รอจนสถานะเป็น **"Connected"** (สีเขียว)
4. ทดสอบฟังก์ชันต่างๆ:
   - พิมพ์คำภาษาไทยในช่อง input
   - กดปุ่ม **"Get Phonemes"** / **"Segment Text"** / **"Analyze"**
   - ดูผลลัพธ์ใน "Standard WebSocket API" section

5. ทดสอบ MCP Protocol:
   - กดปุ่ม **"Initialize"** → ดู protocol version
   - กดปุ่ม **"Tools List"** → ดูรายการ tools
   - กดปุ่ม **"Tools Call"** → ทดสอบเรียกใช้ tool

### วิธีที่ 2: ใช้ Browser Console

เปิด Developer Tools (F12) และรันโค้ดใน Console:

```javascript
// Connect to WebSocket
const socket = io('https://170.64.173.219:2083', {
  rejectUnauthorized: false
});

// Listen for connection
socket.on('connection_response', (data) => {
  console.log('Connected:', data);
});

// Test get_phonemes
socket.emit('get_phonemes', { text: 'สวัสดี' });

// Listen for response
socket.on('phonemes_response', (data) => {
  console.log('Phonemes:', data);
});

// Test MCP Protocol
socket.emit('mcp_request', {
  jsonrpc: "2.0",
  method: "tools/list",
  params: {},
  id: 1
});

socket.on('mcp_response', (data) => {
  console.log('MCP Response:', data);
});
```

---

## 5️⃣ ทดสอบด้วย Postman

### Setup

1. เปิด Postman
2. ไปที่ **Settings** → **SSL certificate verification** → ปิด
3. สร้าง request ใหม่

### Test REST API

- **Method:** GET
- **URL:** `https://170.64.173.219:2083/สวัสดี`
- กด **Send**

### Test MCP SSE

- **Method:** POST
- **URL:** `https://170.64.173.219:2083/mcp/sse`
- **Headers:**
  - `Content-Type: application/json`
- **Body (raw JSON):**
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
  "id": 1
}
```

---

## 6️⃣ Troubleshooting

### ❌ Connection Refused / Timeout

```bash
# ตรวจสอบว่า server เปิดอยู่
ping 170.64.173.219

# ตรวจสอบ port
nmap -p 2083 170.64.173.219

# หรือใช้ telnet
telnet 170.64.173.219 2083
```

### ❌ SSL Certificate Error

ใช้ flag `-k` หรือ `--insecure` กับ curl:
```bash
curl -k https://170.64.173.219:2083/health
```

หรือใน Python:
```python
sio = socketio.Client(ssl_verify=False)
```

### ❌ CORS Error (Browser)

Server รองรับ CORS แล้ว (`cors_allowed_origins="*"`)

ถ้ายังมีปัญหา ให้ตรวจสอบ:
1. ใช้ HTTPS แทน HTTP
2. เช็ค browser console สำหรับ error message
3. ลองใช้ browser อื่น

### ❌ WebSocket Connection Failed

1. ตรวจสอบว่า server รัน SocketIO:
   ```bash
   curl -k https://170.64.173.219:2083/socket.io/
   ```

2. ลอง polling fallback:
   ```javascript
   const socket = io('https://170.64.173.219:2083', {
     transports: ['polling', 'websocket']
   });
   ```

---

## 7️⃣ Performance Testing

### Load Test (Apache Bench)

```bash
# Test REST API
ab -n 1000 -c 10 -k https://170.64.173.219:2083/สวัสดี

# Test MCP endpoint
ab -n 100 -c 5 -p mcp_request.json -T 'application/json' \
   https://170.64.173.219:2083/mcp/sse
```

### WebSocket Load Test

```python
import socketio
import asyncio
from concurrent.futures import ThreadPoolExecutor

def test_websocket():
    sio = socketio.Client(ssl_verify=False)
    sio.connect('https://170.64.173.219:2083')
    sio.emit('get_phonemes', {'text': 'สวัสดี'})
    sio.disconnect()

# Run 100 concurrent connections
with ThreadPoolExecutor(max_workers=100) as executor:
    futures = [executor.submit(test_websocket) for _ in range(100)]
```

---

## 8️⃣ Monitoring

### Check Server Logs (ถ้ามี access)

```bash
# ดู Docker logs
docker logs thai-phonetic-unified -f

# ดู connection count
docker exec thai-phonetic-unified netstat -an | grep :5000 | wc -l
```

### Check Health Periodically

```bash
# ทุก 5 วินาที
watch -n 5 'curl -k -s https://170.64.173.219:2083/health | jq'
```

---

## ✅ Test Checklist

- [ ] Health check ผ่าน
- [ ] REST API ทำงานได้
- [ ] MCP SSE endpoint ตอบกลับถูกต้อง
- [ ] Standard WebSocket events ทำงานได้
- [ ] MCP WebSocket protocol ทำงานได้
- [ ] Browser test ผ่าน
- [ ] ทดสอบกับข้อความยาวๆ
- [ ] ทดสอบ concurrent connections
- [ ] Response time < 1 second

---

## 📊 Expected Performance

- **REST API:** ~100-200ms
- **WebSocket:** ~10-50ms (after connection)
- **Concurrent Users:** 100+ (depends on server resources)
- **Uptime:** 99%+ with Docker restart policy

---

## 🆘 Support

หากพบปัญหา:
1. เช็ค server logs
2. ทดสอบ health endpoint
3. ตรวจสอบ network/firewall
4. ดู error message ใน browser console
5. ลองใช้ test scripts ที่มีให้

## 📝 Notes

- Server ใช้ self-signed certificate ต้องใช้ `-k` flag
- WebSocket URL: `wss://170.64.173.219:2083/socket.io/`
- ทุก endpoint รองรับ HTTPS
- MCP protocol version: `2024-11-05`
