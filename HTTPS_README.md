# HTTPS Configuration

แอปพลิเคชันนี้รองรับ Self-signed HTTPS certificate สำหรับการเข้ารหัสการสื่อสาร

## คุณสมบัติ

- ✅ Self-signed SSL certificate (valid 365 วัน)
- ✅ Auto-generated certificate เมื่อ build Docker image
- ✅ รองรับทั้ง HTTPS และ HTTP fallback
- ✅ รองรับกับ MCP protocol และ Original API

## การใช้งาน

### วิธีที่ 1: ใช้ Docker Compose (แนะนำ)

```bash
# Build และ run ด้วย HTTPS
docker-compose up -d --build

# ทดสอบการเชื่อมต่อ HTTPS
curl -k https://localhost:2083/health
```

### วิธีที่ 2: Build Docker Image แบบ Manual

```bash
# Build image
docker build -t thai-phonetic-https .

# Run container
docker run -d -p 2083:5000 --name thai-phonetic thai-phonetic-https

# ทดสอบการเชื่อมต่อ
curl -k https://localhost:2083/health
```

### วิธีที่ 3: Run แบบ Local (Python)

```bash
# Generate certificate
bash generate_cert.sh

# Run application
python app_unified.py
```

## การทดสอบ

### ทดสอบ HTTPS endpoint

```bash
# Health check
curl -k https://localhost:2083/health

# Original API - Thai word phonetic
curl -k https://localhost:2083/สวัสดี

# MCP endpoint
curl -k -X POST https://localhost:2083/mcp/sse \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

### ทดสอบด้วย Browser

เปิด browser และไปที่:
```
https://localhost:2083/health
```

**หมายเหตุ:** Browser จะเตือนเรื่อง certificate ไม่น่าเชื่อถือ เพราะเป็น self-signed certificate
ให้คลิก "Advanced" และ "Proceed to localhost" เพื่อดำเนินการต่อ

## ไฟล์ที่เกี่ยวข้อง

- `generate_cert.sh` - Script สร้าง SSL certificate
- `app_unified.py` - แอปพลิเคชันที่รองรับ HTTPS
- `Dockerfile` - สร้าง certificate อัตโนมัติเมื่อ build
- `docker-compose.yml` - Config สำหรับ HTTPS

## Certificate Details

- **Algorithm:** RSA 4096-bit
- **Validity:** 365 days
- **Location:** `/app/certs/`
  - Certificate: `/app/certs/cert.pem`
  - Private Key: `/app/certs/key.pem`

## สำหรับ Production

⚠️ **คำเตือน:** Self-signed certificate เหมาะสำหรับ development และ testing เท่านั้น

สำหรับ production แนะนำให้ใช้:
- Let's Encrypt (ฟรี)
- Certificate จาก Certificate Authority ที่น่าเชื่อถือ
- ใช้ reverse proxy เช่น Nginx หรือ Traefik

## Troubleshooting

### Certificate ไม่ถูกสร้าง
```bash
# ตรวจสอบว่า openssl ติดตั้งแล้ว
openssl version

# Run script manually
bash generate_cert.sh
```

### Connection Refused
```bash
# ตรวจสอบว่า container ทำงาน
docker ps

# ตรวจสอบ logs
docker logs thai-phonetic-unified

# ตรวจสอบว่า port ไม่ถูกใช้งาน
netstat -tuln | grep 2083
```

### Browser ไม่ยอมให้เข้าถึง
1. คลิก "Advanced" หรือ "ขั้นสูง"
2. คลิก "Proceed to localhost (unsafe)" หรือ "ดำเนินการต่อไปยัง localhost"
3. หรือใช้ `curl` กับ flag `-k` แทน browser
