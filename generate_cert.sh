#!/bin/bash
# Generate self-signed SSL certificate for HTTPS

# Use /app/certs in Docker, ./certs locally
if [ -w "/app" ]; then
    CERT_DIR="/app/certs"
else
    CERT_DIR="./certs"
fi

CERT_FILE="$CERT_DIR/cert.pem"
KEY_FILE="$CERT_DIR/key.pem"

# Create certs directory if it doesn't exist
mkdir -p $CERT_DIR

# Generate self-signed certificate (valid for 365 days)
openssl req -x509 -newkey rsa:4096 -nodes \
  -out $CERT_FILE \
  -keyout $KEY_FILE \
  -days 365 \
  -subj "/C=TH/ST=Bangkok/L=Bangkok/O=Thai Phonetic/OU=Development/CN=localhost"

# Set proper permissions
chmod 644 $CERT_FILE
chmod 600 $KEY_FILE

echo "Self-signed certificate generated successfully!"
echo "Certificate: $CERT_FILE"
echo "Private Key: $KEY_FILE"
